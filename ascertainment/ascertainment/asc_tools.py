import itertools

def get_SNP_sites(snp_file):
    """Read SNP positions from .bed file as template for pseudo array"""
    fileSNP = open(snp_file, 'r')
    # print "read SNP file"
    SNP = [line for line in fileSNP]
    fileSNP.close()
    return [int(line.split('\t')[2]) for line in SNP]

def set_asc_bits(seq_list, n_asc, pos, site_inds):
    if n_asc == len(site_inds):
        for x in xrange(n_asc):
            for seq in seq_list:
                n = seq.ignore if seq.type == 'discovery' else seq.tot
                bit_list = seq.CGI_bits if seq.type == 'discovery' else seq.bits
                seq.asc_bits.extend( bit_list[ pos[x]*n : pos[x]*n + n ] )
    elif len(site_inds) > n_asc:
        for x in xrange( len(pos) ):
            for seq in seq_list:
                n = seq.ignore if seq.type == 'discovery' else seq.tot
                bit_list = seq.CGI_bits if seq.type == 'discovery' else seq.bits
                seq.asc_bits.extend( bit_list[ site_inds[pos[x]]*n : site_inds[pos[x]]*n + n])

def make_ped_file(file_name, seq_list):
    fileped = open(file_name, 'w')

    for seq in seq_list:
        if seq.type == 'discovery':
            n = seq.ignore
        elif seq.type == 'sample':
            n = seq.tot
        write_ped(fileped, seq, n)
    fileped.close()

def write_ped(fped, sequence, n):
    name = sequence.name

    for indiv in xrange(0, n, 2):
        fped.write(name + ' ' + name + str(indiv / 2 + 1) + '_' + name  + ' 0 0 1 -9 ')
        for bit in itertools.chain.from_iterable( [sequence.asc_bits[i : i+2] for i in xrange(indiv, sequence.asc_bits.length(), n)] ):
            if bit:
                fped.write('2 ')
            else:
                fped.write('1 ')
        fped.write('\n')

def make_map_file(file_name, p_asc, n_c, sites):
    filemap = open(file_name, 'a')

    for asc in p_asc:
        map_str = '{0} chr{0}_{1} {2} {3}\n'.format( n_c, asc, int(sites[asc] - 1), int(sites[asc]) )
        filemap.write(map_str)
    filemap.close()