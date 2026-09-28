from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound

from .models import (
    Academic,
    BoardingRule,
    Holiday,
    ExamSession,
    ExamRoutine,
    ExamInstruction,
    ClassDepartment,
    ClassRoutine,
    DailySchedule,
    CoCurricularActivity,
    BoardingMealMenu,
    BoardingMealTiming,
    BoardingMealRule,
)
from .serializers import (
    AcademicSerializer,
    BoardingRuleSerializer,
    HolidaySerializer,
    ExamSessionSerializer,
    ExamRoutineSerializer,
    ExamInstructionSerializer,
    ClassDepartmentSerializer,
    ClassRoutineSerializer,
    DailyScheduleSerializer,
    CoCurricularActivitySerializer,
    BoardingMealMenuSerializer,
    BoardingMealTimingSerializer,
    BoardingMealRuleSerializer,
)

class CustomPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'
    max_page_size = 100

class AcademicListApiView(generics.ListAPIView):    
    queryset = Academic.objects.all().order_by('id')
    serializer_class = AcademicSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['class_name']
    ordering_fields = ['class_title']
    search_fields = ['class_name', 'class_title']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return Response({
                'success': True,
                'message': 'Classes fetched successfully',
                'count': self.paginator.page.paginator.count,
                'total_pages': self.paginator.page.paginator.num_pages,
                'data': serializer.data,
                'results': serializer.data
            })
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'message': 'Classes fetched successfully',
            'count': queryset.count(),
            'total_pages': 1,
            'data': serializer.data,
            'results': serializer.data
        })

class AcademicDetailsListApiView(generics.RetrieveAPIView):
    queryset = Academic.objects.all()
    serializer_class = AcademicSerializer
    lookup_field = 'pk' 

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except NotFound:
            return Response({'error': 'Class Not Found'}, status=status.HTTP_404_NOT_FOUND)


class BoardingRuleListApiView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = BoardingRuleSerializer
    pagination_class = None

    def get_queryset(self):
        qs = BoardingRule.objects.filter(is_active=True).order_by('rule_number')
        cat = self.request.query_params.get('category')
        if cat and cat != 'all':
            qs = qs.filter(category=cat)
        return qs


class HolidayListApiView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = HolidaySerializer
    pagination_class = None

    def get_queryset(self):
        qs = Holiday.objects.filter(is_active=True).order_by('order')
        year = self.request.query_params.get('year')
        if year:
            qs = qs.filter(academic_year=year)
        cat = self.request.query_params.get('category')
        if cat and cat != 'all':
            qs = qs.filter(category=cat)
        return qs


class ExamSessionListApiView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ExamSessionSerializer
    pagination_class = None

    def get_queryset(self):
        return ExamSession.objects.filter(is_active=True).order_by('order')


class ExamInstructionListApiView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ExamInstructionSerializer
    pagination_class = None

    def get_queryset(self):
        return ExamInstruction.objects.filter(is_active=True).order_by('order')


class ExamRoutineListApiView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ExamRoutineSerializer
    pagination_class = None

    def get_queryset(self):
        qs = ExamRoutine.objects.filter(is_active=True).order_by('order')
        session_id = self.request.query_params.get('session')
        if session_id:
            qs = qs.filter(session_id=session_id)
        jamat_id = self.request.query_params.get('jamat')
        if jamat_id:
            qs = qs.filter(jamat_id=jamat_id)
        return qs


class ExamRoutineJamatsApiView(generics.GenericAPIView):
    """Returns distinct jamats currently having active exam routines"""
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        qs = ExamRoutine.objects.filter(is_active=True).values('jamat_id', 'jamat_name').distinct()
        seen = set()
        jamats = []
        for item in qs:
            if item['jamat_id'] not in seen:
                seen.add(item['jamat_id'])
                jamats.append({'id': item['jamat_id'], 'name': item['jamat_name']})
        return Response({'success': True, 'jamats': jamats})


class ClassDepartmentListApiView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ClassDepartmentSerializer
    pagination_class = None

    def get_queryset(self):
        return ClassDepartment.objects.filter(is_active=True).order_by('order')


class DailyScheduleListApiView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = DailyScheduleSerializer
    pagination_class = None

    def get_queryset(self):
        return DailySchedule.objects.filter(is_active=True).order_by('order')


class ClassRoutineListApiView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ClassRoutineSerializer
    pagination_class = None

    def get_queryset(self):
        qs = ClassRoutine.objects.filter(is_active=True).order_by('order')
        dept = self.request.query_params.get('department')
        if dept:
            qs = qs.filter(department=dept)
        jamat_id = self.request.query_params.get('jamat')
        if jamat_id:
            qs = qs.filter(jamat_id=jamat_id)
        return qs


class ClassRoutineMetaApiView(generics.GenericAPIView):
    """Returns active departments and their available jamats dynamically"""
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        depts_qs = ClassDepartment.objects.filter(is_active=True).order_by('order')
        depts = [
            {
                'id': d.dept_id,
                'name': d.name,
                'desc': d.desc,
                'icon': d.icon,
            }
            for d in depts_qs
        ]

        routines_qs = ClassRoutine.objects.filter(is_active=True).values('department', 'jamat_id', 'jamat_name').distinct()
        jamats_by_dept = {}
        for r in routines_qs:
            dept_key = r['department']
            if dept_key not in jamats_by_dept:
                jamats_by_dept[dept_key] = []
            if not any(j['id'] == r['jamat_id'] for j in jamats_by_dept[dept_key]):
                jamats_by_dept[dept_key].append({'id': r['jamat_id'], 'name': r['jamat_name']})

        return Response({
            'success': True,
            'departments': depts,
            'jamats_by_dept': jamats_by_dept
        })


class CoCurricularListApiView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CoCurricularActivitySerializer
    pagination_class = None

    def get_queryset(self):
        qs = CoCurricularActivity.objects.filter(is_active=True).order_by('order')
        cat = self.request.query_params.get('category')
        if cat and cat != 'all':
            qs = qs.filter(category=cat)
        return qs


class BoardingMealMenuListApiView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = BoardingMealMenuSerializer
    pagination_class = None

    def get_queryset(self):
        return BoardingMealMenu.objects.filter(is_active=True).order_by('order')


class BoardingMealTimingListApiView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = BoardingMealTimingSerializer
    pagination_class = None

    def get_queryset(self):
        return BoardingMealTiming.objects.filter(is_active=True).order_by('order')


class BoardingMealRuleListApiView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = BoardingMealRuleSerializer
    pagination_class = None

    def get_queryset(self):
        return BoardingMealRule.objects.filter(is_active=True).order_by('order')
