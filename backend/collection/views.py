from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import NotFound
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import LegoSet
from .serializers import LegoSetSerializer, UserSerializer
from .rebrickable_api import get_lego_set_price


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["post"])
    def register(self, request):
        """Permet de créer un utilisateur via l'API"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Utilisateur créé avec succès"},
                status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LegoSetViewSet(viewsets.ModelViewSet):
    queryset = LegoSet.objects.all()
    serializer_class = LegoSetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Affiche uniquement les sets appartenant à l'utilisateur connecté."""
        return LegoSet.objects.filter(user=self.request.user)
    
    def get_object(self):
        """Récupère l'objet et renvoie une erreur 403 si l'utilisateur n'est pas propriétaire."""
        try:
            obj = super().get_object()
        except NotFound:
            raise NotFound(detail="Set not found")

        # Vérifie si l'utilisateur est bien le propriétaire
        if obj.user != self.request.user:
            self.permission_denied(self.request, message="Accès non autorisé")

        return obj

    def perform_create(self, serializer):
        """Associe automatiquement le set LEGO à l'utilisateur connecté."""
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        """Empêche un utilisateur de modifier un set qui ne lui appartient pas."""
        instance = self.get_object()
        if instance.user != request.user:
            return Response(
                {"error": "Modification non autorisée"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Empêche un utilisateur de supprimer un set qui ne lui appartient pas."""
        instance = self.get_object()
        if instance.user != request.user:
            return Response(
                {"error": "Suppression non autorisée"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
    
        @action(detail=False, methods=["get"])
        def total_value(self, request):
            """Retourne la valeur totale de la collection LEGO de l'utilisateur."""
            total_price = LegoSet.objects.filter(user=request.user).aggregate(Sum("price"))["price__sum"]
            return Response({"total_value": total_price or 0})

        @action(detail=True, methods=["post"])
        def update_price(self, request, pk=None):
            """Met à jour le prix d'un set spécifique."""
            lego_set = self.get_object()
            lego_set.update_price()
            return Response({"message": f"Prix mis à jour: {lego_set.price} €"})
