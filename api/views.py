from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Project, ProjectPlace
from .serializers import (
    ProjectSerializer,
    CreateProjectSerializer,
    AddPlaceSerializer,
    UpdatePlaceSerializer,
)
from .services.artic_api import get_artwork


@api_view(['GET', 'POST'])
def project_list(request):
    if request.method == 'GET':
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    serializer = CreateProjectSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    place_ids = serializer.validated_data.pop('place_ids', [])

    project = Project.objects.create(**serializer.validated_data)

    for external_id in place_ids:
        artwork = get_artwork(external_id)
        if not artwork:
            project.delete()
            return Response(
                {"error": f"Place {external_id} not found in Art Institute API."},
                status=status.HTTP_400_BAD_REQUEST
            )
        ProjectPlace.objects.create(project=project, **artwork)

    return Response(ProjectSerializer(project).data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'DELETE', 'PATCH'])
def project_detail(request, pk):
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(ProjectSerializer(project).data)
    if request.method == 'PATCH':
        serializer = CreateProjectSerializer(project, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.validated_data.pop('place_ids', None)
        for attr, value in serializer.validated_data.items():
            setattr(project, attr, value)
        project.save()
        return Response(ProjectSerializer(project).data)

    if request.method == 'DELETE':
        if project.places.filter(is_visited=True).exists():
            return Response(
                {"error": "Cannot delete project with visited places."},
                status=status.HTTP_400_BAD_REQUEST
            )
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','POST'])
def place_list(request, project_pk):
    try:
        project = Project.objects.get(pk=project_pk)
    except Project.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        places = project.places.all()
        from .serializers import ProjectPlaceSerializer
        return Response(ProjectPlaceSerializer(places, many=True).data)

    if project.places.count() >= 10:
        return Response(
            {"error": "Project already has maximum 10 places."},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = AddPlaceSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    external_id = serializer.validated_data['external_id']

    if project.places.filter(external_id=external_id).exists():
        return Response(
            {"error": "Place already exists in this project."},
            status=status.HTTP_400_BAD_REQUEST
        )

    artwork = get_artwork(external_id)
    if not artwork:
        return Response(
            {"error": f"Place {external_id} not found in Art Institute API."},
            status=status.HTTP_400_BAD_REQUEST
        )

    place = ProjectPlace.objects.create(project=project, **artwork)
    from .serializers import ProjectPlaceSerializer
    return Response(ProjectPlaceSerializer(place).data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PATCH'])
def place_detail(request, project_pk, place_pk):
    try:
        project = Project.objects.get(pk=project_pk)
        place = project.places.get(pk=place_pk)
    except (Project.DoesNotExist, ProjectPlace.DoesNotExist):
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        from .serializers import ProjectPlaceSerializer
        return Response(ProjectPlaceSerializer(place).data)

    serializer = UpdatePlaceSerializer(place, data=request.data, partial=True)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()

    if not project.places.filter(is_visited=False).exists():
        project.is_completed = True
        project.save()

    from .serializers import ProjectPlaceSerializer
    return Response(ProjectPlaceSerializer(place).data)



