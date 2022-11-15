from datetime import datetime
import os
import shutil
import gzip

src_path='/cifs/RWIS/midotmet.dat'
dst_dir = '/home/wwwgrr/scripts/rwis'
now = datetime.utcnow()
now_str = datetime.strftime(now, "%Y%m%d_%H00")
dst_fn = "RWIS_" + now_str + ".dat.gz"
dst_path = os.path.join(dst_dir,dst_fn)

with src_path.open(mode='rb') as f_in:
    with gzip.open(dst_path,'wb') as f_out:
        shutil.copyfileobj(f_in,f_out)