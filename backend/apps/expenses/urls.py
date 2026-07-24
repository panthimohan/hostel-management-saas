from rest_framework.routers import DefaultRouter

from .views import ExpenseViewSet, IncomeViewSet

router = DefaultRouter()
router.register("incomes", IncomeViewSet, basename="income")
router.register("", ExpenseViewSet, basename="expense")

urlpatterns = router.urls
