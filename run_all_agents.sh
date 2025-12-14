uvicorn services.planner.main:app --host 0.0.0.0 --port 8001 &
uvicorn services.codegen.main:app --host 0.0.0.0 --port 8002 &
uvicorn services.executor.main:app --host 0.0.0.0 --port 8003 &
uvicorn services.evaluator.main:app --host 0.0.0.0 --port 8004 &
uvicorn services.evolve.main:app --host 0.0.0.0 --port 8005 &
uvicorn api.run_etl:app --host 0.0.0.0 --port 9000 --reload
wait