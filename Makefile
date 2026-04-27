up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f

seed-demo:
	docker compose exec -T backend python /app/scripts/bootstrap_demo.py
