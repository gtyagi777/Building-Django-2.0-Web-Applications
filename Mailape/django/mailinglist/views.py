
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, DetailView
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse

from mailinglist.models import MailingList, Message, Subscriber
from mailinglist.forms import MailingListForm, SubscriberForm, MessageForm
from mailinglist.mixins import UserCanUseMailingList

class MailingListListView(LoginRequiredMixin, ListView):

    def get_queryset(self):
        return MailingList.objects.filter(owner=self.request.user)


class CreateMailingListView(LoginRequiredMixin, CreateView):
    form_class = MailingListForm
    template_name = "mailinglist/mailinglist_form.html"

    def get_initial(self):
        return {
            'owner': self.request.user.id
        }


class DeleteMailingListView(LoginRequiredMixin, UserCanUseMailingList, DeleteView):
    model = MailingList
    success_url = reverse_lazy('mailinglist:mailinglist_list')


class MailingListDetailView(LoginRequiredMixin, UserCanUseMailingList, DetailView):
    model = MailingList

    def get_object(self):
        return MailingList.objects.get(pk=self.kwargs['pk'])



class SubscribeToMailingListView(CreateView):
    form_class = SubscriberForm
    template_name = 'mailinglist/subscriber_form.html'

    def get_initial(self):
        return {
            'mailing_list': self.kwargs['pk']
        }
    
    def get_success_url(self):
        return reverse('mailinglist:subscriber_thankyou', kwargs={
            'pk': self.object.mailing_list.id
        })
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        mailing_list_id = self.kwargs['pk']
        ctx['mailing_list'] = get_object_or_404(
            MailingList,
            id=mailing_list_id
        )
        return ctx


class ThankYouForSubsribingView(DetailView):
    model = MailingList
    template_name = 'mailinglist/subscription_thankyou.html'


class ConfirmSubsriiptionView(DetailView):
    model = Subscriber
    template_name = 'mailinglist/confirm_subscription.html'

    def get_object(self, queryset=None):
        subscriber = super().get_object(queryset=queryset)
        subscriber.confirmed = True
        subscriber.save()
        return subscriber


class UnsubscribeView(DeleteView):
    model = Subscriber
    template_name = 'mailinglist/unsubscribe.html'

    def get_success_url(self):
        mailing_list = self.object.mailing_list
        return reverse('mailinglist:subscribe', kwargs={
            'pk': mailing_list.id
        })


class CreateMessageView(LoginRequiredMixin, CreateView):
    SAVE_ACTION = 'save'
    PREVIEW_ACTION = 'preview'

    form_class = MessageForm
    template_name = 'mailinglist/message_form.html'

    def get_success_url(self):
        return reverse('mailinglist:manage_mailinglist',
                        kwargs={'pk': self.object.mailing_list.id})
    
    def get_initial(self):
        mailing_list = self.get_mailing_list()
        return {
            'mailing_list': mailing_list.id
        }
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        mailing_list = self.get_mailing_list()
        ctx.update({
            'mailing_list': mailing_list,
            'SAVE_ACTION': self.SAVE_ACTION,
            'PREVIEW_ACTION': self.PREVIEW_ACTION
        })
        return ctx
    
    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == self.PREVIEW_ACTION:
            context = self.get_context_data(
                form=form,
                message=form.instance
            )
            return self.render_to_response(context=context)
        elif action == self.SAVE_ACTION:
            return super().form_valid(form)
    
    def get_mailing_list(self):
        mailing_list = get_object_or_404(MailingList, id=self.kwargs['pk'])

        if not mailing_list.user_can_use_mailing_list(self.request.user):
            raise PermissionError()
        return mailing_list


class MessageDetailView(LoginRequiredMixin, UserCanUseMailingList,
                        DetailView):
    model = Message


#
# Mailing REST API
#

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from mailinglist.permissions import CanUseMailingList
from mailinglist.serializers import ( 
    MailingListSerializer, SubscriberSerializer, ReadOnlyEmailSubscriberSerializer
)


class MailingListCreateListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, CanUseMailingList)
    serializer_class   = MailingListSerializer

    def get_queryset(self):
        return self.request.user.mailinglist_set.all()
    
    def get_serializer(self, *args, **kwargs):
        if kwargs.get('data', None):
            data = kwargs.get('data', None)
            owner = {
                'owner': self.request.user.id
            }
            data.update(owner)
        
        return super().get_serializer(*args, **kwargs)


class MailingListRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, CanUseMailingList)
    serializer_class = MailingListSerializer
    queryset = MailingList.objects.all()


class SubscriberCreateListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, CanUseMailingList)
    serializer_class   = SubscriberSerializer

    def get_queryset(self):
        mailing_list_pk = self.kwargs['mailing_list_pk']
        mailing_list = get_object_or_404(MailingList, id=mailing_list_pk)
        return mailing_list.subscriber_set.all()
    
    def get_serializer(self, *args, **kwargs):
        if kwargs.get('data', None):
            data = kwargs.get('data', None)
            mailing_list = {
                'mailing_list': reverse(
                    'mailinglist:api-mailing-list-detail',
                    kwargs={'pk': self.kwargs['mainling_list_pk']}
                )
            }
            data.update(mailing_list)
        
        return super().get_serializer(*args, **kwargs)


class SubscriberRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, CanUseMailingList)
    serializer_class = ReadOnlyEmailSubscriberSerializer
    queryset = Subscriber.objects.all()