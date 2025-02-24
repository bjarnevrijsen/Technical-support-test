from django.core.management.base import BaseCommand
from ...models import Vessel
from django.db import transaction
import threading


class Command(BaseCommand):
    help = "Simulate condition when withdrawing refrigerant from a vessel."

    def handle(self, *args, **kwargs):
        Vessel.objects.create(name="Test Vessel", content=50.0)
        self.stdout.write("Simulating condition...")
        self.run_simulation()

    def run_simulation(self):
        barrier = threading.Barrier(2)

        def user_withdraw():
            barrier.wait()
            with transaction.atomic():
                vessel = Vessel.objects.select_for_update().get(id=1)
                if vessel.content >= 10.0:
                    vessel.content -= 10.0
                    vessel.save()
                else:
                  self.stdout.write("the vessel is empty and further withdrawals are not possible")


        t1 = threading.Thread(target=user_withdraw)
        t2 = threading.Thread(target=user_withdraw)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        vessel = Vessel.objects.get(id=1)
        self.stdout.write(f"Remaining content: {vessel.content} kg")
