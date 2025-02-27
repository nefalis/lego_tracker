from rest_framework import viewsets, permissions
from .models import LegoSet
from .serializers import LegoSetSerializer


class LegoSetViewSet(viewsets.ModelViewSet):
    queryset = LegoSet.objects.all()
    serializer_class = LegoSetSerializer
    # Seuls les utilisateurs connectés ont accès
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Affiche uniquement les sets de l'utilisateur
        return LegoSet.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Associe le set LEGO à l'utilisateur connecté
        serializer.save(user=self.request.user)
