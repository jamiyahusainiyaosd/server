from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import FormerStudent
from .serializers import FormerStudentSerializer

def api_success(data=None, message="Success", meta=None):
    payload = {"success": True, "message": message, "data": data}
    if meta is not None:
        payload["meta"] = meta
    return payload


def api_error(message="Error", errors=None):
    payload = {"success": False, "message": message}
    if errors is not None:
        payload["errors"] = errors
    return payload

class SimplePaginator:
    default_page_size = 12
    max_page_size = 100

    def paginate(self, queryset, request):
        try:
            page = int(request.query_params.get("page", 1))
        except ValueError:
            page = 1

        try:
            page_size = int(request.query_params.get("page_size", self.default_page_size))
        except ValueError:
            page_size = self.default_page_size

        page_size = max(1, min(page_size, self.max_page_size))
        if page < 1:
            page = 1

        total = queryset.count()
        offset = (page - 1) * page_size
        items = queryset[offset: offset + page_size]

        meta = {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": (total + page_size - 1) // page_size,
        }
        return items, meta


paginator = SimplePaginator()

class FormerStudentListCreateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        qs = FormerStudent.objects.all()

        pass_year = request.query_params.get("pass_year")
        if pass_year:
            try:
                qs = qs.filter(pass_year=int(pass_year))
            except ValueError:
                return Response(api_error("Invalid pass_year"), status=status.HTTP_400_BAD_REQUEST)

        search = request.query_params.get("search")
        if search:
            search = search.strip()
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(address__icontains=search) |
                Q(current__icontains=search) |
                Q(mobile__icontains=search)
            )

        ordering = request.query_params.get("ordering", "-created_at")
        allowed = {"created_at", "-created_at", "name", "-name", "pass_year", "-pass_year"}
        if ordering not in allowed:
            return Response(
                api_error("Invalid ordering", {"allowed": sorted(list(allowed))}),
                status=status.HTTP_400_BAD_REQUEST
            )
        qs = qs.order_by(ordering)

        items, meta = paginator.paginate(qs, request)
        data = FormerStudentSerializer(items, many=True).data
        return Response(api_success(data=data, meta=meta), status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = FormerStudentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(api_error("Validation failed", serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        obj = serializer.save()
        return Response(api_success(FormerStudentSerializer(obj).data, "Created"), status=status.HTTP_201_CREATED)

class FormerStudentDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, formerStudent_id):
        try:
            return FormerStudent.objects.get(id=formerStudent_id)
        except FormerStudent.DoesNotExist:
            return None

    def get(self, request, formerStudent_id, *args, **kwargs):
        obj = self.get_object(formerStudent_id)
        if not obj:
            return Response(api_error("Not found"), status=status.HTTP_404_NOT_FOUND)
        return Response(api_success(FormerStudentSerializer(obj).data), status=status.HTTP_200_OK)

    def put(self, request, formerStudent_id, *args, **kwargs):
        obj = self.get_object(formerStudent_id)
        if not obj:
            return Response(api_error("Not found"), status=status.HTTP_404_NOT_FOUND)
        serializer = FormerStudentSerializer(obj, data=request.data)
        if not serializer.is_valid():
            return Response(api_error("Validation failed", serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        obj = serializer.save()
        return Response(api_success(FormerStudentSerializer(obj).data, "Updated"), status=status.HTTP_200_OK)

    def patch(self, request, formerStudent_id, *args, **kwargs):
        obj = self.get_object(formerStudent_id)
        if not obj:
            return Response(api_error("Not found"), status=status.HTTP_404_NOT_FOUND)
        serializer = FormerStudentSerializer(obj, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(api_error("Validation failed", serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        obj = serializer.save()
        return Response(api_success(FormerStudentSerializer(obj).data, "Updated"), status=status.HTTP_200_OK)

    def delete(self, request, formerStudent_id, *args, **kwargs):
        obj = self.get_object(formerStudent_id)
        if not obj:
            return Response(api_error("Not found"), status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response(api_success(message="Deleted"), status=status.HTTP_204_NO_CONTENT)