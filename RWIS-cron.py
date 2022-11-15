from datetime import datetime
import os
import shutil
import gzip
#from pathlib import Path

src_path='/cifs/RWIS/midotmet.dat'
#src = Path(src_path)
dst_dir = '/home/wwwgrr/scripts/rwis'
now = datetime.utcnow()
now_str = datetime.strftime(now, "%Y%m%d_%H00")
dst_fn = "RWIS_" + now_str + ".dat.gz"
dst_path = os.path.join(dst_dir,dst_fn)

f_in = open(src_path,'rb')
f_out = gzip.open(dst_path,'wb')
shutil.copyfileobj(f_in,f_out)
