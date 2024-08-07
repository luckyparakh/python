up:
	sudo docker-compose up -d
down:
	sudo docker-compose down
activate:
	source venv/bin/activate
deactivate:
	source deactivate
firstrun: down up
	sleep 120
	uvicorn app.main:app --reload
run:
	uvicorn app.main:app --reload

misc:
	sudo docker exec -it cassandra1 cqlsh -e "CREATE KEYSPACE IF NOT EXISTS video_membership_app WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : '1' };"
	sudo docker exec -it cassandra1 cqlsh -e "SELECT * FROM video_membership_app.user;"