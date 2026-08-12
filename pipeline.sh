#!/bin/sh

echo "========================================"
echo "PayFlow Pipeline Orchestrator Started"
echo "========================================"

while true
do

    echo ""
    echo "========================================"
    echo "Running Bronze -> Silver"
    echo "========================================"

    /opt/spark/bin/spark-submit \
        /opt/spark-apps/silver_transform.py

    if [ $? -ne 0 ]; then
        echo "Silver transformation FAILED."
        echo "Skipping Gold and PostgreSQL for this cycle."
        echo "Retrying in 30 seconds..."
        sleep 30
        continue
    fi

    echo "Silver transformation completed successfully."


    echo ""
    echo "========================================"
    echo "Running Silver -> Gold"
    echo "========================================"

    /opt/spark/bin/spark-submit \
        /opt/spark-apps/gold_transform.py

    if [ $? -ne 0 ]; then
        echo "Gold transformation FAILED."
        echo "Skipping PostgreSQL for this cycle."
        echo "Retrying in 30 seconds..."
        sleep 30
        continue
    fi

    echo "Gold transformation completed successfully."


    echo ""
    echo "========================================"
    echo "Running Gold -> PostgreSQL"
    echo "========================================"

    /opt/spark/bin/spark-submit \
        --jars /opt/spark-ivy/cache/org.postgresql/postgresql/jars/postgresql-42.7.7.jar \
        /opt/spark-apps/gold_to_postgres.py

    if [ $? -ne 0 ]; then
        echo "Gold -> PostgreSQL FAILED."
        echo "Retrying in 30 seconds..."
        sleep 30
        continue
    fi

    echo "Gold -> PostgreSQL completed successfully."


    echo ""
    echo "========================================"
    echo "Pipeline complete."
    echo "Waiting 30 seconds before next run..."
    echo "========================================"

    sleep 30

done