from rest_framework import generics
from consumer.models import Consumer
from consumer.serializers import ConsumerSerializer

class ConsumerListAPIView(generics.ListAPIView):
    serializer_class = ConsumerSerializer

    def get_queryset(self):
        queryset = Consumer.objects.all()

        # Filter by min_previous_jobs_count parameter
        min_previous_jobs_count = self.request.query_params.get('min_previous_jobs_count')
        if min_previous_jobs_count is not None:
            queryset = queryset.filter(previous_jobs_count__gte=min_previous_jobs_count)

        # Filter by max_previous_jobs_count parameter
        max_previous_jobs_count = self.request.query_params.get('max_previous_jobs_count')
        if max_previous_jobs_count is not None:
            queryset = queryset.filter(previous_jobs_count__lte=max_previous_jobs_count)

        # Filter by previous_jobs_count parameter
        previous_jobs_count = self.request.query_params.get('previous_jobs_count')
        if previous_jobs_count is not None:
            queryset = queryset.filter(previous_jobs_count=previous_jobs_count)

        # Filter by status parameter
        status = self.request.query_params.get('status')
        if status is not None:
            queryset = queryset.filter(status=status)

        return queryset


class ConsumerDetailView(generics.RetrieveAPIView):
    queryset = Consumer.objects.all()
    serializer_class = ConsumerSerializer
    lookup_field = 'pk'