from setuptools import setup, Extension
setup(
    name = 'wxpay',
    packages = ['wxpay'],
    version = '0.13',
    description = 'a lib for wechat payment',
    author = 'sivacohan',
    author_email = 'sivacohan@gmail.com',
    url = 'https://github.com/SIvaCoHan/wxpay',
    keywords = ['wechat', 'payment', 'library'],
    install_requires = [
        'dict2xml>=1.3',
        'qrcode>=5.1',
        # 'Pillow>=2.7.0',
        'requests>=2.6.1',
    ],
    classifiers = [],
)
