import json


def create_dot_file(dependencies_data):
    """Создает DOT файл для Graphviz"""
    dot_content = ['digraph matplotlib_dependencies {',
                   '  rankdir=TB;',
                   '  node [shape=box, style=filled, fillcolor=lightblue];',
                   '  "matplotlib";',
                   '']

    # Добавляем зависимости
    for package, deps in dependencies_data.items():
        for dep in deps:
            dot_content.append(f'  "{package}" -> "{dep}";')

    dot_content.append('}')

    return '\n'.join(dot_content)


def main():
    print("СОЗДАНИЕ DOT-ФАЙЛА ДЛЯ MATPLOTLIB")
    print("=" * 40)

    try:
        # Читаем зависимости из JSON файла
        with open("dependencies.json", "r", encoding="utf-8") as f:
            dependencies = json.load(f)

        # Создаем и сохраняем DOT файл
        dot_content = create_dot_file(dependencies)
        with open("matplotlib_dependencies.dot", "w", encoding="utf-8") as f:
            f.write(dot_content)

        print("DOT-файл создан: matplotlib_dependencies.dot")

        # Инструкция по использованию Graphviz
        print("\nИНСТРУКЦИЯ ПО ИСПОЛЬЗОВАНИЮ GRAPHVIZ:")
        print("-" * 40)
        print("Для преобразования в PNG выполните:")
        print("   dot -Tpng matplotlib_dependencies.dot -o graph.png")
        print("\nЕсли не работает, используйте полный путь:")
        print('   "C:\\Program Files\\Graphviz\\bin\\dot.exe" -Tpng matplotlib_dependencies.dot -o graph.png')

    except FileNotFoundError:
        print("Ошибка: Файл dependencies.json не найден.")
        print("Сначала запустите get_dependencies.py для получения данных о зависимостях.")
    except Exception as e:
        print(f"Ошибка при создании DOT-файла: {e}")


if __name__ == "__main__":
    main()