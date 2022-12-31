from dataclasses import field

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from .models import Conversation, Message, Participant, TextMessage, get_message_content


class ContentTypeSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return "%s.%s" % (value.app_label, value.model)

    def to_internal_value(self, data):
        if isinstance(data, str):
            try:

                app_label, model = data.split(".")
                if (
                    content_type := ContentType.objects.filter(
                        app_label=app_label, model=model
                    ).first()
                ) is not None:
                    return content_type
            except:
                pass

        raise serializers.ValidationError("invalid")

    def get_queryset(self):
        return ContentType.objects.filter(**{"model__in": get_message_content()})


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "firstname"]


class ConversationSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, data=empty, has_message=True, **kwargs):
        super().__init__(instance, data, **kwargs)

        self.has_message = has_message

    def get_fields(self):
        fields = super().get_fields()

        if "message" not in fields and self.has_message:
            fields["message"] = serializers.SerializerMethodField(read_only=True)

        if (
            self.context
            and (request := self.context.get("request")) is not None
            and request.method == "POST"
        ):
            # pass
            fields["participants"] = serializers.ManyRelatedField(
                child_relation=serializers.PrimaryKeyRelatedField(
                    # read_only=True,
                    queryset=get_user_model()
                    .objects.filter(is_staff=False, is_superuser=False, is_active=True)
                    .all(),
                ),
            )
        return fields

    def get_message(self, obj):
        message = obj.messages.first()

        if not message:
            return None

        return MessageSerializer(message).data

    def save(self, **kwargs):
        instance: Conversation = super().save(**kwargs)

        if (request := self.context.get("request")) is not None and request.user:
            Participant(
                user=request.user, role=Participant.Role.ADMIN, conversation=instance
            ).save()
            instance.participants.add(request.user)
        return instance

    class Meta:
        model = Conversation
        fields = [
            "id",
            "name",
            "conversation_type",
            # "message",
            # "participants",
            "created_at",
            "updated_at",
        ]


class TextMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextMessage
        fields = ["content"]


class MessageObjectRelatedField(serializers.RelatedField):

    serializer_classes = [TextMessageSerializer]

    def to_representation(self, value):
        for serializer_class in self.serializer_classes:
            if isinstance(value, serializer_class.Meta.model):
                serializers = TextMessageSerializer(value)
                return serializers.data
        else:
            raise Exception("Unexpected type of tagged object")

    def get_queryset(self):
        return super().get_queryset()

    def to_internal_value(self, data):

        if (
            self.parent
            and (content_type := self.parent.initial_data.get("content_type"))
            is not None
        ):
            instance = self.parent.instance.detail if self.parent.instance else None

            for serializer_class in self.serializer_classes:
                model_class = serializer_class.Meta.model

                if content_type == TextMessage._meta.label_lower:
                    serializer = serializer_class(instance=instance, data=data)

                    if serializer.is_valid():
                        if instance is None:
                            instance = model_class()

                        for attr, value in serializer.validated_data.items():
                            setattr(instance, attr, value)
                        return instance

            else:
                raise serializers.ValidationError("content type is invalid")

        raise serializers.ValidationError("content type is missing")
        # return super().to_internal_value(data)


class RecursiveSerializer(serializers.RelatedField):
    def to_representation(self, value):
        # if value is not None:
        #     return self.parent.__class__(value).data
        return None

    def get_queryset(self):
        return self.parent.Meta.model.objects.all()


class MessageSerializer(serializers.ModelSerializer):
    content_type = ContentTypeSerializer()
    content_object = MessageObjectRelatedField()

    # reply = RecursiveSerializer()

    class Meta:
        model = Message
        fields = [
            "id",
            "conversation",
            "sender",
            "reply",
            "content_type",
            # "object_id",
            "detail",
            "created_at",
            "updated_at",
        ]

    def to_representation(self, instance):
        if self.parent and not self.parent.parent:
            self.fields["reply"] = MessageSerializer(read_only=True)
        return super(MessageSerializer, self).to_representation(instance)

    def create(self, validated_data):
        if (detail := validated_data.get("detail")) is not None:
            detail.save()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if (detail := validated_data.get("detail")) is not None:
            detail.save()
        return super().update(instance, validated_data)

    def get_reply(self, obj):
        if obj.reply is not None:
            return MessageSerializer(obj.reply).data
        return None

    # def to_representation(self, value):

    #     if (value.detail, TextMessage):
    #         value.detail = TextMessageSerializer(value.detail).data

    #     else:
    #         raise Exception("Unexpected type of tagged object")

    #     return super().to_representation(value)


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["pk", "username", "first_name", "last_name"]
