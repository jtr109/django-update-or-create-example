import threading
import uuid

from django.test import TestCase

from .models import Race, Solution, Together


class RaceTestCase(TestCase):

    def test_race(self):
        ''' 测试会发生数据竞争的情况

        预期 threading 报错: race.models.Race.MultipleObjectsReturned: get() returned more than one Race -- it returned 2!
        '''

        def get_or_create():
            Race.objects.get_or_create(
                user_id='c53b8ba212ef4f15b2365e1bb3d524fe',
                defaults=dict(name='foo', age=1),
            )

        threads = list()
        for _ in range(10):
            threads.append(threading.Thread(target=get_or_create))
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        self.assertNotEqual(Race.objects.count(), 1)

    def test_resolve_with_unique(self):
        ''' 测试加入 unique 资源后解决 data race condition
        '''

        def get_or_create():
            Solution.objects.get_or_create(
                user_id='c53b8ba212ef4f15b2365e1bb3d524fe',
                defaults=dict(name='foo', age=1),
            )

        threads = list()
        for _ in range(10):
            threads.append(threading.Thread(target=get_or_create))
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        self.assertEqual(Solution.objects.count(), 1)

    def test_unreloved_without_unique_together(self):
        ''' 测试只有一列 unique 但是以两列为基准 `get_or_create` 的情况
        '''

        def get_or_create(name):
            Race.objects.get_or_create(
                user_id='c53b8ba212ef4f15b2365e1bb3d524fe',
                name=name,  # 'user_0' or 'user_1'
                defaults=dict(age=1),
            )

        threads = list()
        for i  in range(10):
            threads.append(threading.Thread(target=get_or_create, args=(f'user_{i%2}',)))
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        self.assertNotEqual(Race.objects.count(), 2)

    def test_resolve_by_unique_together(self):
        ''' 测试 `unique_together`
        '''

        def get_or_create(name):
            Together.objects.get_or_create(
                user_id='c53b8ba212ef4f15b2365e1bb3d524fe',
                name=name,  # 'user_0' or 'user_1'
                defaults=dict(age=1),
            )

        threads = list()
        for i  in range(10):
            threads.append(threading.Thread(target=get_or_create, args=(f'user_{i%2}',)))
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        self.assertEqual(Together.objects.count(), 2)

