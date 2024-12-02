.PHONY: test test-user test-note test-date

# 设置 Django 环境变量
export DJANGO_SETTINGS_MODULE=backend.settings

test:
	python manage.py test

test-user:
	python manage.py test user.tests

test-note:
	python manage.py test note.tests

test-date:
	python manage.py test date.tests