#!/bin/bash

celery -A Library.celery_app worker -B -l INFO -Q send_mail,newsletter
