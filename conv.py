import os
import subprocess

def get_dst_size(size):
    dst_size = 300
    if size > 1000 and size <= 1400:
        dst_size = 250
    elif size > 600 and size <= 1000:
        dst_size = 200
    elif size > 400 and size <= 600:
        dst_size = 150
    elif size > 100 and size <= 400:
        dst_size = 120
    elif size < 100:
        dst_size = size
    return dst_size

def get_prj_str(dst_size):
    s = 'adm = Avidemux()\r\n\
adm.setPostProc(3, 3, 0)\r\n\
adm.videoCodec("x264", "useAdvancedConfiguration=True", "general.params=2PASS=???",\r\n\
"general.threads=0", "general.preset=ultrafast", "general.tuning=none",\r\n\
"general.profile=baseline","general.fast_decode=False", "general.zero_latency=False",\r\n\
"general.fast_first_pass=True", "general.blueray_compatibility=False",\r\n\
"general.fake_interlaced=False", "level=-1", "vui.sar_height=1", "vui.sar_width=1",\r\n\
"MaxRefFrames=3", "MinIdr=25", "MaxIdr=250",\r\n\
"i_scenecut_threshold=40", "intra_refresh=False", "MaxBFrame=3", "i_bframe_adaptive=1",\r\n\
"i_bframe_bias=0", "i_bframe_pyramid=2", "b_deblocking_filter=True", "i_deblocking_filter_alphac0=0", "i_deblocking_filter_beta=0",\r\n\
"cabac=True", "interlaced=False", "constrained_intra=False", "tff=True", "fake_interlaced=False",\r\n\
"analyze.b_8x8=True", "analyze.b_i4x4=True", "analyze.b_i8x8=True", "analyze.b_p8x8=True", "analyze.b_p16x16=False",\r\n\
"analyze.b_b16x16=False", "analyze.weighted_pred=2", "analyze.weighted_bipred=True", "analyze.direct_mv_pred=1",\r\n\
"analyze.chroma_offset=0", "analyze.me_method=1", "analyze.me_range=16", "analyze.mv_range=-1",\r\n\
"analyze.mv_range_thread=-1", "analyze.subpel_refine=7", "analyze.chroma_me=True", "analyze.mixed_references=True",\r\n\
"analyze.trellis=1", "analyze.psy_rd=1.000000", "analyze.psy_trellis=0.000000", "analyze.fast_pskip=True",\r\n\
"analyze.dct_decimate=True", "analyze.noise_reduction=0", "analyze.psy=True", "analyze.intra_luma=11",\r\n\
"analyze.inter_luma=21", "ratecontrol.rc_method=0", "ratecontrol.qp_constant=0", "ratecontrol.qp_min=10",\r\n\
"ratecontrol.qp_max=51", "ratecontrol.qp_step=4", "ratecontrol.bitrate=0", "ratecontrol.rate_tolerance=1.000000",\r\n\
"ratecontrol.vbv_max_bitrate=0", "ratecontrol.vbv_buffer_size=0", "ratecontrol.vbv_buffer_init=1",\r\n\
"ratecontrol.ip_factor=1.400000", "ratecontrol.pb_factor=1.300000", "ratecontrol.aq_mode=1",\r\n\
"ratecontrol.aq_strength=1.000000", "ratecontrol.mb_tree=True", "ratecontrol.lookahead=40")\r\n\
adm.audioClearTracks()\r\n\
adm.setSourceTrackLanguage(0,"und")\r\n\
adm.audioAddTrack(0)\r\n\
adm.audioCodec(0, "copy");\r\n\
adm.audioSetDrc(0, 0)\r\n\
adm.audioSetShift(0, 0, 0)\r\n\
adm.setContainer("MP4", "muxerType=0", "optimize=1", "forceAspectRatio=False", "aspectRatio=1", "rotation=0", "clockfreq=0")\r\n\
'.replace('???', str(dst_size))                                                                                                                                                                                                                                                   
    return s 


def get_file_list(thisdir, ext):
    flist = []
    for r, d, f in os.walk(thisdir):
        for file in f:
            if file.endswith(ext):
                flist.append(os.path.join(r, file))
    return flist

def silentremove(filename):
    try:
        os.remove(filename)
    except OSError:
        pass


def main():
    thisdir = os.getcwd()
    flist = get_file_list(thisdir, ".MTS")
    for src in flist:
        dst_size = get_dst_size(os.path.getsize(src) // (2**20))
        prj_str = get_prj_str(dst_size) 
        prj_name = 'prj264.py'
        with open(prj_name, 'w') as f:
            f.write(prj_str)
        dst = src[:-3] + 'mp4'
        silentremove(dst+'.stats')
        silentremove(dst+'.stats.mbtree')
        silentremove(src+'.idx2')
        os.system('"c:/soft/Avidemux 2.7 VC++ 64bits/avidemux_cli.exe" --load '+ src + ' --run ' + prj_name + ' --save ' + dst + ' --quit')
        silentremove(dst+'.stats')
        silentremove(dst+'.stats.mbtree')
        silentremove(src+'.idx2')
        silentremove(src)

if __name__ == '__main__':
    main()
