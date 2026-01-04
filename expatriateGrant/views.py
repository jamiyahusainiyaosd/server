from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly  

from .models import ExpatriateGrant
from .serializers import ExpatriateGrantSerializer

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

class ExpatriateGrantListCreateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        qs = ExpatriateGrant.objects.all()

        member_type = request.query_params.get("member_type")
        if member_type:
            qs = qs.filter(member_type=member_type)

        donor_status = request.query_params.get("status")
        if donor_status:
            qs = qs.filter(status=donor_status)

        search = request.query_params.get("search")
        if search:
            search = search.strip()
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(address__icontains=search) |
                Q(mobile__icontains=search)
            )
        ordering = request.query_params.get("ordering", "-created_at")
        allowed = {"created_at", "-created_at", "name", "-name", "status", "-status", "member_type", "-member_type"}
        if ordering not in allowed:
            return Response(
                api_error("Invalid ordering", {"allowed": sorted(list(allowed))}),
                status=status.HTTP_400_BAD_REQUEST
            )
        qs = qs.order_by(ordering)

        items, meta = paginator.paginate(qs, request)
        data = ExpatriateGrantSerializer(items, many=True).data
        return Response(api_success(data=data, meta=meta), status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ExpatriateGrantSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(api_error("Validation failed", serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        obj = serializer.save()
        return Response(api_success(ExpatriateGrantSerializer(obj).data, "Created"), status=status.HTTP_201_CREATED)

class ExpatriateGrantDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, expatriategrant_id):
        try:
            return ExpatriateGrant.objects.get(id=expatriategrant_id)
        except ExpatriateGrant.DoesNotExist:
            return None

    def get(self, request, expatriategrant_id, *args, **kwargs):
        obj = self.get_object(expatriategrant_id)
        if not obj:
            return Response(api_error("Not found"), status=status.HTTP_404_NOT_FOUND)
        return Response(api_success(ExpatriateGrantSerializer(obj).data), status=status.HTTP_200_OK)

    def put(self, request, expatriategrant_id, *args, **kwargs):
        obj = self.get_object(expatriategrant_id)
        if not obj:
            return Response(api_error("Not found"), status=status.HTTP_404_NOT_FOUND)
        serializer = ExpatriateGrantSerializer(obj, data=request.data)
        if not serializer.is_valid():
            return Response(api_error("Validation failed", serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        obj = serializer.save()
        return Response(api_success(ExpatriateGrantSerializer(obj).data, "Updated"), status=status.HTTP_200_OK)

    def patch(self, request, expatriategrant_id, *args, **kwargs):
        obj = self.get_object(expatriategrant_id)
        if not obj:
            return Response(api_error("Not found"), status=status.HTTP_404_NOT_FOUND)
        serializer = ExpatriateGrantSerializer(obj, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(api_error("Validation failed", serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        obj = serializer.save()
        return Response(api_success(ExpatriateGrantSerializer(obj).data, "Updated"), status=status.HTTP_200_OK)

    def delete(self, request, expatriategrant_id, *args, **kwargs):
        obj = self.get_object(expatriategrant_id)
        if not obj:
            return Response(api_error("Not found"), status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response(api_success(message="Deleted"), status=status.HTTP_204_NO_CONTENT)