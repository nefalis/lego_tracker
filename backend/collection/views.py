from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import LegoSet
from .serializers import LegoSetSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["post"])
    def register(self, request):
        """Permet de créer un utilisateur via l'API"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Utilisateur créé avec succès"}, status=201)
        return Response(serializer.errors, status=400)


class LegoSetViewSet(viewsets.ModelViewSet):
    queryset = LegoSet.objects.all()
    serializer_class = LegoSetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Affiche uniquement les sets appartenant à l'utilisateur connecté."""
        return LegoSet.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Associe automatiquement le set LEGO à l'utilisateur connecté."""
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        """Empêche un utilisateur de modifier un set qui ne lui appartient pas."""
        instance = self.get_object()
        if instance.user != request.user:
            return Response({"error": "Modification non autorisée"}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Empêche un utilisateur de supprimer un set qui ne lui appartient pas."""
        instance = self.get_object()
        if instance.user != request.user:
            return Response({"error": "Suppression non autorisée"}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
