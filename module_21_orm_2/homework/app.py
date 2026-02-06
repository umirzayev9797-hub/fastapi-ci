import csv
import io
from flask import Flask, request, jsonify
from db.database import SessionLocal
from models.library import Student

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/students/upload', methods=['POST'])
def upload_students_csv():
    """
    Профессиональная массовая вставка студентов из CSV.
    """
    # 1. Проверяем, прикрепил ли пользователь файл
    if 'file' not in request.files:
        return jsonify({"error": "Файл не найден в запросе"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "Файл не выбран"}), 400

    db = SessionLocal()
    try:
        # 2. Читаем файл в текстовом режиме без сохранения на диск
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)

        # 3. Используем DictReader с разделителем ';'
        reader = csv.DictReader(stream, delimiter=';')

        # Подготавливаем данные (конвертируем типы из строк в нужные форматы)
        students_to_insert = []
        for row in reader:
            students_to_insert.append({
                "name": row['name'],
                "surname": row['surname'],
                "phone": row['phone'],
                "email": row['email'],
                "average_score": float(row['average_score']),
                "scholarship": row['scholarship'].lower() == 'true'
            })

        # 4. Массовая вставка (Bulk Insert)
        if students_to_insert:
            db.bulk_insert_mappings(Student, students_to_insert)
            db.commit()
            return jsonify({"message": f"Успешно импортировано {len(students_to_insert)} студентов"}), 201

        return jsonify({"message": "Файл пуст"}), 200

    except Exception as e:
        db.rollback()
        return jsonify({"error": f"Ошибка при обработке: {str(e)}"}), 500
    finally:
        db.close()


if __name__ == '__main__':
    app.run(debug=True)