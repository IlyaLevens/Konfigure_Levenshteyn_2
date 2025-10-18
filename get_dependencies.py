import subprocess
import sys
import json


def install_and_run_pipdeptree():
    """Устанавливает и запускает pipdeptree для matplotlib"""
    try:
        # Устанавливаем pipdeptree если не установлен
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "pipdeptree"],
            capture_output=True,
            check=True
        )

        # Получаем дерево зависимостей в JSON формате
        result = subprocess.run(
            [sys.executable, "-m", "pipdeptree", "-p", "matplotlib", "-j"],
            capture_output=True,
            text=True,
            check=True
        )

        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Ошибка: {e}")
        return None


def parse_dependencies(json_output):
    """Парсит JSON вывод pipdeptree"""
    try:
        data = json.loads(json_output)
        dependencies = {}

        for item in data:
            package_name = item['package']['key'].replace('_', '-')
            dependencies[package_name] = []

            for dep in item['dependencies']:
                dep_name = dep['key'].replace('_', '-')
                dependencies[package_name].append(dep_name)

                # Рекурсивно добавляем под-зависимости
                if 'dependencies' in dep:
                    for sub_dep in dep['dependencies']:
                        sub_dep_name = sub_dep['key'].replace('_', '-')
                        if dep_name not in dependencies:
                            dependencies[dep_name] = []
                        dependencies[dep_name].append(sub_dep_name)

        return dependencies
    except Exception as e:
        print(f"Ошибка парсинга JSON: {e}")
        return {}


def main():
    print("ПОЛУЧЕНИЕ ЗАВИСИМОСТЕЙ MATPLOTLIB")
    print("=" * 40)

    # Получаем дерево через pipdeptree в JSON формате
    json_output = install_and_run_pipdeptree()

    if json_output:
        # Парсим зависимости
        dependencies = parse_dependencies(json_output)

        # Сохраняем зависимости в JSON файл для использования в другом скрипте
        with open("dependencies.json", "w", encoding="utf-8") as f:
            json.dump(dependencies, f, indent=2)

        # Выводим текстовое дерево
        print("\nДЕРЕВО ЗАВИСИМОСТЕЙ:")
        print("-" * 30)
        for package, deps in dependencies.items():
            print(f"{package}")
            for dep in deps:
                print(f"  └── {dep}")

        # Сохраняем в текстовый файл
        with open("matplotlib_dependencies.txt", "w", encoding="utf-8") as f:
            f.write("Дерево зависимостей matplotlib\n")
            f.write("=" * 40 + "\n")
            for package, deps in dependencies.items():
                f.write(f"{package}\n")
                for dep in deps:
                    f.write(f"  └── {dep}\n")

        print(f"\nТекстовый результат сохранен в: matplotlib_dependencies.txt")
        print(f"Данные для DOT файла сохранены в: dependencies.json")

    else:
        print("Не удалось получить дерево зависимостей")


if __name__ == "__main__":
    main()