from rest_framework import viewsets
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# from rest_framework.generics import CreateAPIView, DestroyAPIView
# from rest_framework.permissions import IsAuthenticated
from django.urls import reverse_lazy
from .models import Ad, ExchangeProposal
from .serializers import AdSerializer, ExchangeProposalSerializer, serializers
from .forms import AdForm, SignUpForm, ExchangeProposalForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.core.paginator import Paginator
# API Views

class ExchangeProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeProposal
        fields = '__all__'
        read_only_fields = ('status',)

# class ExchangeProposalCreateAPIView(CreateAPIView):
#     queryset = ExchangeProposal.objects.all()
#     serializer_class = ExchangeProposalSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(
#             ad_sender_id=self.request.data.get('sender_ad_id'),
#             ad_receiver_id=self.kwargs['pk'],
#             status='pending'
#         )

class AdSearchView(ListView):
    model = Ad
    template_name = 'ads/list.html'  # Используем тот же шаблон, что и для списка
    context_object_name = 'ads'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        category = self.request.GET.get('category')
        condition = self.request.GET.get('condition')

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(description__icontains=search_query)
            )

        if category:
            queryset = queryset.filter(category=category)

        if condition:
            queryset = queryset.filter(condition=condition)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['categories'] = Ad.CATEGORY_CHOICES
        context['conditions'] = Ad.CONDITION_CHOICES
        return context

class ExchangeProposalListView(LoginRequiredMixin, ListView):
    model = ExchangeProposal
    template_name = 'ads/exchange_proposals.html'
    context_object_name = 'proposals'
    
    # def get_queryset(self):
    #     return ExchangeProposal.objects.filter(
    #         ad_receiver__user=self.request.user
    #     ).select_related('ad_sender', 'ad_receiver')
    
    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset.filter(ad_receiver__user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем количество непросмотренных предложений
        context['unread_proposals_count'] = ExchangeProposal.objects.filter(
            ad_receiver__user=self.request.user,
            status='pending'
        ).count()
        return context

def accept_exchange_proposal(request, pk):
        proposal = get_object_or_404(ExchangeProposal, pk=pk, ad_receiver__user=request.user)
        proposal.status = 'accepted'
        proposal.save()
        return redirect('ads:exchange_proposals')

def reject_exchange_proposal(request, pk):
        proposal = get_object_or_404(ExchangeProposal, pk=pk, ad_receiver__user=request.user)
        proposal.status = 'rejected'
        proposal.save()
        return redirect('ads:exchange_proposals')
    
        
class ExchangeProposalCreateView(LoginRequiredMixin, CreateView):
    model = ExchangeProposal
    form_class = ExchangeProposalForm  # Используем форму вместо fields
    template_name = 'ads/propose_exchange.html'
    
    def form_valid(self, form):
        form.instance.ad_receiver = get_object_or_404(Ad, id=self.kwargs['ad_id'])
        form.instance.ad_sender = get_object_or_404(Ad, id=self.request.GET.get('sender_ad_id'))
        form.instance.status = 'pending'
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('ads:detail', kwargs={'pk': self.kwargs['ad_id']})
    


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all().order_by('-created_at')
    serializer_class = AdSerializer

class ExchangeProposalViewSet(viewsets.ModelViewSet):
    queryset = ExchangeProposal.objects.all()
    serializer_class = ExchangeProposalSerializer
    
    

# Template Views
class AdListView(ListView):
    model = Ad
    template_name = 'ads/list.html'
    context_object_name = 'ads'
    paginate_by = 10

class AdDetailView(DetailView):
    model = Ad
    template_name = 'ads/detail.html'  # Указываем шаблон

    def get_context_data(self, **kwargs):
        # Получаем стандартный контекст
        context = super().get_context_data(**kwargs)
        
        # Добавляем объявление текущего пользователя (если есть)
        if self.request.user.is_authenticated:
            context['user_ad'] = Ad.objects.filter(
                user=self.request.user
            ).first()  # Берём первое объявление пользователя
        
        return context

class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad
    form_class = AdForm
    template_name = 'ads/create.html'
    success_url = reverse_lazy('ads:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class AdUpdateView(LoginRequiredMixin, UpdateView):
    model = Ad
    form_class = AdForm
    template_name = 'ads/edit.html'
    success_url = reverse_lazy('ads:list')

    def get_queryset(self):
        """Ограничиваем доступ только к своим объявлениям"""
        return super().get_queryset().filter(user=self.request.user)
    
    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("Вы не автор объявления")
        instance.delete()
        
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


        
# class AdDeleteAPIView(DestroyAPIView):
#     queryset = Ad.objects.all()
#     serializer_class = AdSerializer
#     permission_classes = [IsAuthenticated]


class AdDeleteView(LoginRequiredMixin, DeleteView):
    model = Ad
    template_name = 'ads/delete.html'
    success_url = reverse_lazy('ads:list')
    

    def get_queryset(self):
        """Ограничиваем доступ только к своим объявлениям"""
        return super().get_queryset().filter(user=self.request.user)
    
    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("Вы не автор объявления")
        instance.delete()
    
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')