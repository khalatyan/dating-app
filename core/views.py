import jwt

from django.shortcuts import render
from django.conf import settings
from django.contrib import auth
from django.core.mail import send_mail
from django.template import loader

from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend

from core.serializers import UserSerializer, LoginSerializer, EstimationSerializer, UserDetailSerializer
from core.models import *
from core.service import UserFilter

class RegisterView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        email = data.get('email', '')
        password = data.get('password', '')
        user = auth.authenticate(email=email, password=password)

        if user:
            auth_token = jwt.encode(
                {'email': user.email}, settings.JWT_SECRET_KEY, algorithm="HS256")
            serializer = UserSerializer(user)
            data = {'user': serializer.data, 'token': auth_token}
            return Response(data, status=status.HTTP_200_OK)

        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class EstimationView(GenericAPIView):
    serializer_class = EstimationSerializer

    def post(self, request, pk):
        who_was_rated = User.objects.filter(id=pk).first()
        if not who_was_rated:
            return Response({"error": "Такого участника не существует"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = EstimationSerializer(data=request.data)
        if serializer.is_valid():
            encoded_jwt = serializer.data.get('jwt', '')
            decoded_jwt = jwt.decode(encoded_jwt, settings.JWT_SECRET_KEY, algorithms=["HS256"])
            if 'email' in decoded_jwt:
                who_rated = User.objects.filter(email=decoded_jwt['email']).first()
                if not who_rated:
                    return Response(status=status.HTTP_403_FORBIDDEN)

                # Сохраняем оценку
                estimation = Estimation.objects.filter(
                    who_rated=who_rated,
                    who_was_rated=who_was_rated
                ).first()
                if not estimation:
                    estimation = Estimation.objects.create(
                        who_rated=who_rated,
                        who_was_rated=who_was_rated,
                        estimation=serializer.data.get('estimation')
                    )
                else:
                    estimation.estimation = serializer.data.get('estimation')
                estimation.save()

                # Проверка на взаимную симпатию
                if estimation.estimation == 1:
                    mutual_estimation = Estimation.objects.filter(
                        who_rated=who_was_rated,
                        who_was_rated=who_rated
                    ).first()
                    if mutual_estimation and mutual_estimation.estimation == 1:
                        data = {
                            "message": f"Почта участника: {who_was_rated.email}"
                        }

                        # Отправляем сообщение о взимной симпатии на почты участнмков
                        send_mutual_sympathy_message(who_rated, who_was_rated)
                        send_mutual_sympathy_message(who_was_rated, who_rated)

                        return Response(data, status=status.HTTP_201_CREATED)

                # Если взимной симпатии не было установлено, просто принимаем оценку
                data = {
                    "message": f"Ваша оценка принята"
                }
                return Response(data, status=status.HTTP_201_CREATED)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(ListAPIView):
    serializer_class = UserDetailSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserFilter

    def get_queryset(self):
        self_request_user = self.request.user
        max_distance = None
        min_distance = None
        if 'max_distance' in self.request.query_params and self.request.query_params.get('max_distance') != "":
            max_distance = float(self.request.query_params.get('max_distance'))
        if 'min_distance' in self.request.query_params and self.request.query_params.get('min_distance') != "":
            min_distance = float(self.request.query_params.get('min_distance'))

        users = User.objects.all()
        if max_distance or min_distance:
            for user in users:
                if max_distance and user.get_user_distance(self_request_user) > max_distance:
                    users = users.exclude(id=user.id)
                if min_distance and user.get_user_distance(self_request_user) < min_distance:
                    users = users.exclude(id=user.id)
        return users

    # def get_queryset(self):
    #     return


def send_mutual_sympathy_message(user1, user2):
    message_template = loader.get_template('messages/mutual_sympathy_message.txt')

    message_context = {
        'user': user1,
    }
    message = message_template.render(message_context)

    subject = 'Взаимная сипатия!'
    try:
        send_mail(subject, message, 'example@dating-app.ru', [user2.email],
                  fail_silently=False)
    except:
        pass