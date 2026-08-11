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

if [ $? -eq 0 ]; then
    echo "Silver transformation completed successfully."
else
    echo "Silver transformation FAILED."
fi


echo ""
echo "========================================"
echo "Running Silver -> Gold"
echo "========================================"

/opt/spark/bin/spark-submit \
    /opt/spark-apps/gold_transform.py

if [ $? -eq 0 ]; then
    echo "Gold transformation completed successfully."
else
    echo "Gold transformation FAILED."
fi


echo ""
echo "========================================"
echo "Running Gold -> PostgreSQL"
echo "========================================"

/opt/spark/bin/spark-submit \
    --jars /opt/spark-ivy/cache/org.postgresql/postgresql/jars/postgresql-42.7.7.jar \
    /opt/spark-apps/gold_to_postgres.py

if [ $? -eq 0 ]; then
    echo "Gold -> PostgreSQL completed successfully."
else
    echo "Gold -> PostgreSQL FAILED."
fi


echo ""
echo "========================================"
echo "Pipeline complete."
echo "Waiting 30 seconds before next run..."
echo "========================================"

sleep 30

done