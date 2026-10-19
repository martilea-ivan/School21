import asyncio
import aiohttp
import aiofiles
import os
from pathlib import Path
from urllib.parse import urlparse
from prettytable import PrettyTable


class ImageDownloader:
    def __init__(self):
        self.results = []
        self.save_path = None
        self.session = None

    def get_filename_from_url(self, url: str) -> str:
        parsed = urlparse(url)
        filename = os.path.basename(parsed.path)
        if not filename:
            filename = url.replace('/', '_').replace(':', '_')[:50] + '.jpg'
        return filename

    def get_safe_filename(self, url: str) -> str:
        filename = self.get_filename_from_url(url)
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename

    async def download_image(self, url: str, session: aiohttp.ClientSession) -> dict:
        filename = self.get_safe_filename(url)
        filepath = os.path.join(self.save_path, filename)

        try:
            async with session.get(url, timeout=30) as response:
                if response.status == 200:
                    content_type = response.headers.get('content-type', '')
                    if 'image' not in content_type:
                        return {
                            'url': url,
                            'status': 'Ошибка',
                            'filename': filename,
                            'error': f'Не изображение (Content-Type: {content_type})'
                        }

                    async with aiofiles.open(filepath, 'wb') as f:
                        await f.write(await response.read())

                    return {
                        'url': url,
                        'status': 'Успех',
                        'filename': filename,
                        'error': None
                    }
                else:
                    return {
                        'url': url,
                        'status': 'Ошибка',
                        'filename': filename,
                        'error': f'HTTP {response.status}'
                    }
        except asyncio.TimeoutError:
            return {
                'url': url,
                'status': 'Ошибка',
                'filename': filename,
                'error': 'Превышено время ожидания'
            }
        except aiohttp.ClientError as e:
            return {
                'url': url,
                'status': 'Ошибка',
                'filename': filename,
                'error': f'Ошибка соединения: {str(e)[:50]}'
            }
        except Exception as e:
            return {
                'url': url,
                'status': 'Ошибка',
                'filename': filename,
                'error': f'Неизвестная ошибка: {str(e)[:50]}'
            }

    async def download_all(self, urls: list):
        connector = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = [self.download_image(url, session) for url in urls]
            self.results = await asyncio.gather(*tasks)

    def print_summary(self):
        print("\n" + "=" * 80)
        print("  СВОДКА ОБ УСПЕШНЫХ И НЕУСПЕШНЫХ ЗАГРУЗКАХ")
        print("=" * 80)

        table = PrettyTable(["Ссылка", "Статус"])
        table.align["Ссылка"] = "l"

        for result in self.results:
            status = result['status']
            url = result['url']
            if len(url) > 70:
                url = url[:67] + "..."
            table.add_row([url, status])

        print(table)
        print("=" * 80)


def validate_path(path: str) -> bool:
    try:
        path_obj = Path(path)
        if not path_obj.exists():
            path_obj.mkdir(parents=True, exist_ok=True)
        test_file = path_obj / '.test_write'
        test_file.touch()
        test_file.unlink()
        return True
    except Exception:
        return False


def get_save_path() -> str:
    while True:
        path = input("Введите путь для сохранения изображений: ").strip()
        if not path:
            print("Путь не может быть пустым. Попробуйте снова.")
            continue
        if validate_path(path):
            return path
        else:
            print("Некорректный путь или нет доступа для записи. Попробуйте снова.")


def get_urls() -> list:
    print("\nВводите ссылки на изображения (пустая строка для завершения):")
    urls = []
    while True:
        url = input().strip()
        if not url:
            break
        urls.append(url)
    return urls


async def main():
    print("=" * 60)
    print("  СКАЧИВАНИЕ ИЗОБРАЖЕНИЙ")
    print("=" * 60)
    print()

    save_path = get_save_path()
    print(f"Изображения будут сохранены в: {save_path}")

    urls = get_urls()

    if not urls:
        print("Не введено ни одной ссылки. Завершение программы.")
        return

    print(f"\nНачинаем загрузку {len(urls)} изображений...")

    downloader = ImageDownloader()
    downloader.save_path = save_path

    await downloader.download_all(urls)

    downloader.print_summary()


if __name__ == "__main__":
    asyncio.run(main())