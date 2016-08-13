# -*- mode: python -*-
a = Analysis(['train_ticket'],
             pathex=['D:\\pyinstaller-2.0'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'train_ticket.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=True )
