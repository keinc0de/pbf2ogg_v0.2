from pathlib import Path


class ArchivoPbf:
    def __init__(self, video=None):
        self.asigna_video(video)
        self.thumb = None

    def asigna_video(self, video):
        pbf = Path(video).with_suffix('.pbf').as_posix()
        self.ruta = pbf if Path(pbf).exists() else None

    def _lee(self):
        with open(self.ruta, encoding='utf-16') as txt:
            return [l.strip('\n') for l in txt.readlines()]
        
    def decode(self):
        data = []
        lineas = self._lee()
        if '[Bookmark]' in lineas[0]:
            for linea in lineas:
                if '*' in linea:
                    _, data_linea = linea.strip('\x00').split('=')
                    mseg, titulo, image = data_linea.split('*')
                    d_tiempo = self.mseg_a_tiempo(mseg)
                    img = bytes.fromhex(image.rsplit('0'*43)[-1])
                    data.append({
                        'mseg':int(mseg), 'titulo':titulo,
                        'imagen hex':img, **d_tiempo
                    })
        return data

    def mseg_a_hms(self, msec):
        h, r = divmod(int(msec), 3.6e6)
        m, r = divmod(r, 6e4)
        s, _ = divmod(r, 1e3)
        return int(h), int(m), int(s), int(_)
    
    def mseg_a_tiempo(self, msec):
        h, m, s, ms = self.mseg_a_hms(msec)
        tm = f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"
        t = tm[3::] if tm.startswith('00:') else tm
        return {
            'horas':h, 'mimutos':m, 'segundos':s, 'milisegundos':ms,
            'tiempo':tm, 't':t
        }

