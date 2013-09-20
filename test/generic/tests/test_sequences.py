#coding: utf-8

from decimal import Decimal
from django.test import TestCase
from model_mommy import mommy
from model_mommy.recipe import Recipe, foreign_key, RecipeForeignKey
from model_mommy.timezone import now
from model_mommy.exceptions import InvalidQuantityException
from test.generic.models import Person, DummyNumbersModel, DummyBlankFieldsModel, Dog


from model_mommy.sequences import incr, itera, Sequence


class TestIncrementalSequence(TestCase):
    def test_integer(self):
        people = mommy.make(Person, name=incr(1), _quantity=3)
        self.assertEqual(Person.objects.count(), 3)
        self.assertItemsEqual(
            Person.objects.values_list('name', flat=True), ['2', '3', '4']
        )

    def test_integer_increment_by(self):
        people = mommy.make(Person, name=incr(1, increment_by=2), _quantity=3)
        self.assertEqual(Person.objects.count(), 3)
        self.assertItemsEqual(
            Person.objects.values_list('name', flat=True), ['3', '5', '7']
        )

    def test_string(self):
        people = mommy.make(Person, name=incr('test'), _quantity=3)
        self.assertEqual(Person.objects.count(), 3)
        self.assertItemsEqual(
            Person.objects.values_list('name', flat=True), ['test1', 'test2', 'test3']
        )

    def test_string_increment_by(self):
        people = mommy.make(Person, name=incr('test', increment_by=2), _quantity=3)
        self.assertEqual(Person.objects.count(), 3)
        self.assertItemsEqual(
            Person.objects.values_list('name', flat=True), ['test2', 'test4', 'test6']
        )


class TestIterableSequence(TestCase):
    def test_list(self):
        names = ['Alice', 'Bob', 'Cris']

        # matching args
        people = mommy.make(Person, name=itera(names), _quantity=3)
        self.assertEqual(Person.objects.count(), 3)
        self.assertItemsEqual(
            Person.objects.values_list('name', flat=True), names
        )

        Person.objects.all().delete()

        # mismatching args
        people = mommy.make(Person, name=itera(names), _quantity=5)
        self.assertEqual(Person.objects.count(), 5)
        self.assertItemsEqual(
            Person.objects.values_list('name', flat=True),
            ['Alice', 'Bob', 'Cris', 'Alice', 'Bob']
        )

    def test_tuple(self):
        names = ('Alice', 'Bob', 'Cris')

        # matching args
        people = mommy.make(Person, name=itera(names), _quantity=3)
        self.assertEqual(Person.objects.count(), 3)
        self.assertItemsEqual(
            Person.objects.values_list('name', flat=True), names
        )

        Person.objects.all().delete()

        # mismatching args
        people = mommy.make(Person, name=itera(names), _quantity=5)
        self.assertEqual(Person.objects.count(), 5)
        self.assertItemsEqual(
            Person.objects.values_list('name', flat=True),
            ['Alice', 'Bob', 'Cris', 'Alice', 'Bob']
        )

    def test_string(self):
        names = 'abc'

        # matching args
        people = mommy.make(Person, name=itera(names), _quantity=3)
        self.assertEqual(Person.objects.count(), 3)
        self.assertItemsEqual(
            Person.objects.values_list('name', flat=True), ['a', 'b', 'c']
        )

        Person.objects.all().delete()

        # mismatching args
        people = mommy.make(Person, name=itera(names), _quantity=5)
        self.assertEqual(Person.objects.count(), 5)
        self.assertItemsEqual(
            Person.objects.values_list('name', flat=True),
            ['a', 'b', 'c', 'a', 'b']
        )


class TestSequence(TestCase):
    def test_list(self):
        names = ['Alice', 'Bob', 'Cris']

        # matching args
        people = mommy.make(Person, name=Sequence(names), _quantity=3)
        self.assertEqual(Person.objects.count(), 3)
        self.assertItemsEqual(
            Person.objects.values_list('name', flat=True), names
        )

    def test_string(self):
        people = mommy.make(Person, name=Sequence('test', increment_by=2), _quantity=3)
        self.assertEqual(Person.objects.count(), 3)
        self.assertItemsEqual(
            Person.objects.values_list('name', flat=True), ['test2', 'test4', 'test6']
        )

    def test_integer(self):
        people = mommy.make(Person, name=Sequence(1, increment_by=2), _quantity=3)
        self.assertEqual(Person.objects.count(), 3)
        self.assertItemsEqual(
            Person.objects.values_list('name', flat=True), ['3', '5', '7']
        )
