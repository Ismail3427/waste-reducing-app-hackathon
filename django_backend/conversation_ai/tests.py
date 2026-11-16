from django.test import TestCase

from backend.user.models import User

from .models import Conversation, Message


class ConversationMessageOwnershipTests(TestCase):
    def test_messages_are_scoped_to_their_conversation(self):
        user = User.objects.create(userId="user-1", userEmail="user@example.com")
        first_conversation = Conversation.objects.create(user=user)
        second_conversation = Conversation.objects.create(user=user)
        first_message = Message.objects.create(
            conversation=first_conversation, role="user", content="First"
        )
        second_message = Message.objects.create(
            conversation=second_conversation, role="user", content="Second"
        )

        self.assertEqual(
            list(first_conversation.thread.values_list("pk", flat=True)),
            [first_message.pk],
        )
        self.assertEqual(
            list(second_conversation.thread.values_list("pk", flat=True)),
            [second_message.pk],
        )
