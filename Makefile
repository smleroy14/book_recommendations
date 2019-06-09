book-env/bin/activate: requirements.txt
	test -d book-env || virtualenv book-env
	. book-env/bin/activate; pip install -r requirements.txt
	touch book-env/bin/activate

data/raw_from_s3/books.csv: config.yml src/get_data.py src/load_data_s3.py
	. book-env/bin/activate; python src/get_data.py --config=config.yml --input=michel-avc-project --output=data/raw_from_s3/ 
	. book-env/bin/activate; python src/load_data_s3.py --config=config.yml --input=data/raw_from_s3/ --output=michel-avc-project-private

data/books_w_genres.csv: config.yml src/gen_features.py
	. book-env/bin/activate; python src/gen_features.py --config=config.yml --input=michel-avc-project-private --output=data/books_w_genres.csv

data/recs/all_recs.csv: data/books_w_genres.csv src/train_model.py config.yml
	. book-env/bin/activate; python src/train_model.py --config=config.yml --input=data/books_w_genres.csv --output=data/recs/all_recs.csv

data/model_accuracy.txt: data/books_w_genres.csv src/score_model.py config.yml
	. book-env/bin/activate; python src/score_model.py --config=config.yml --input=data/books_w_genres.csv  --output=data/model_accuracy.txt 


venv: book-env/bin/activate
transfer_data: data/raw_from_s3/books.csv
gen_features: data/books_w_genres.csv
train_model: data/recs/all_recs.csv
score_model: data/model_accuracy.txt

all: venv transfer_data gen_features train_model score_model 

