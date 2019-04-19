#!/bin/bash
CMD=$1

# Wait until postgres is ready
until nc -z $DATABASE_HOST 5432; do
    echo "$(date) - waiting for postgres..."
    sleep 3
done

setup_django () {
    echo Running migrations
    python manage.py migrate --noinput

    echo Create dummy user if none exists
    python manage.py create_superuser_if_none_exists --user=admin --password=admin

    echo Collecting static-files
    python manage.py collectstatic --noinput

}

case "$CMD" in
    "runserver" )
        setup_django

        echo Starting using manage.py runserver
        exec python manage.py runserver 0.0.0.0:8000
        ;;
    * )
        # Run custom command. Thanks to this line we can still use
        # "docker run our_container /bin/bash" and it will work
        exec $CMD ${@:2}
        ;;
esac
