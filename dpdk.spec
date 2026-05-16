# TODO:
# - kernel part (igb_uio module)
# - dlpack <https://github.com/dmlc/dlpack>, dlmc-core <https://github.com/dmlc/dmlc-core>, Apache TVM >= 0.10.0 <https://github.com/apache/tvm>, tvmdp <https://github.com/MarvellEmbeddedProcessors/tvmdp> for drivers/ml/cnxk
# - flexran_sdk for drivers/baseband/turbo_sw
#   (AVX2: libturbo, libcrc, librate_matching, libcommon, libstdc++, libirc, libimf, libipps, libsvml;
#    AVX512: libldpc_encoder_5gnr, libldpc_decoder_5gnr, libLDPC_ratematch_5gnr, librate_dematching_5gnr)
#   https://software.intel.com/content/www/us/en/develop/articles/flexran-lte-and-5g-nr-fec-software-development-kit-modules.html (x86_64, proprietary)
# - musdk (libmusdk) for drivers/common/mvep, drivers/crypto/mvsam, drivers/net/{mvneta,mvpp2}
#   https://github.com/MarvellEmbeddedProcessors/musdk-marvell (aarch64?)
# - libIPSec_MB for drivers/crypto/{aesni_gcm,aesni_mb,kasumi,snow3g,zuc}
#   https://github.com/intel/intel-ipsec-mb (x86_64 only)
# - libAArch64crypto for drivers/crypto/armv8
#   https://github.com/ARM-software/AArch64cryptolib (aarch64)
# - pkgconfig(libwd), pkgconfig(libwd_crypto) for drivers/crypto/uadk
# + pkgconfig(libwd), pkgconfig(libwd_comp) for drivers/compress/uadk
#   https://github.com/Linaro/uadk
# - cuda for drivers/gpu/cuda
# - pkgconfig(netcope-common) for driver/net/nfb
#   https://www.netcope.com/en/company/community-support/dpdk-libsze2 or https://www.liberouter.org/repo/dcpro/base/ - x86_64 only
#   some old versions at https://homeproj.cesnet.cz/rpm/liberouter/{devel,stable}/SRPMS/
#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	esmi		# AMD EPYC SMI support

%ifnarch %{ix86} %{x8664} x32
%undefine	with_esmi
%endif
Summary:	Data Plane Development Kit libraries
Summary(pl.UTF-8):	Biblioteki Data Plane Development Kit
Name:		dpdk
Version:	26.03
Release:	1
License:	BSD (libraries and drivers), GPL v2 (kernel components)
Group:		Libraries
Source0:	https://fast.dpdk.org/rel/%{name}-%{version}.tar.xz
# Source0-md5:	5ef5da0574619860b77871a822e6a6dd
Patch0:		%{name}-time.patch
Patch1:		%{name}-no-mandb.patch
URL:		https://www.dpdk.org/
# pkgconfig(libelf)
BuildRequires:	elfutils-devel
%{?with_esmi:BuildRequires:	esmi_ib_library-devel}
# C11
BuildRequires:	gcc >= 6:4.7
%ifarch aarch64
BuildRequires:	gcc >= 6:4.8.6
%endif
BuildRequires:	jansson-devel
# bpftool
BuildRequires:	kernel-tools
BuildRequires:	libarchive-devel
BuildRequires:	libbpf-devel >= 1.0
BuildRequires:	libbsd-devel
BuildRequires:	libfdt-devel
BuildRequires:	libibverbs-devel
BuildRequires:	libibverbs-driver-mana-devel
BuildRequires:	libibverbs-driver-mlx4-devel
BuildRequires:	libibverbs-driver-mlx5-devel
BuildRequires:	libisal-devel
BuildRequires:	libpcap-devel
BuildRequires:	libxdp-devel >= 1.2.2
# vduse etc.
BuildRequires:	linux-libc-headers >= 7:5.15
BuildRequires:	meson >= 0.57.2
# libmtcl_ul for mlx5
BuildRequires:	mstflint-devel >= 4.31
BuildRequires:	ninja >= 1.5
BuildRequires:	numactl-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 3
BuildRequires:	python3-elftools
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xxd
BuildRequires:	xz
BuildRequires:	zlib-devel
%if %{with apidocs}
BuildRequires:	doxygen
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg >= 2.0
%endif
%ifarch %{ix86} %{x8664} x32
Requires:	cpuinfo(sse4_2)
%endif
# probably R: neon for ARM, altivec for PPC?
ExclusiveArch:	%{ix86} %{x8664} x32 %{arm} aarch64 ppc64
ExcludeArch:	i386 i486 i586 pentium3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		abi_ver		26
%define		lib_ver		%{abi_ver}.1

# non-function symbols per_lcore__lcore_id, per_lcore__rte_errno, per_lcore__thread_id, per_lcore_dpaa_io, per_lcore__dpaa2_io, per_lcore_held_bufs, per_lcore_dpaa2_held_bufs
%define		skip_post_check_so	librte_acl.so.* librte_bbdev.so.* librte_bpf.so.* librte_compressdev.so.* librte_cryptodev.so.* librte_dispatcher.so.* librte_distributor.so.* librte_dma_cnxk.so.* librte_dma_dpaa2.so.* librte_dma_ioat.so.* librte_dmadev.so.* librte_efd.so.* librte_eventdev.so.* librte_ethdev.so.* librte_fib.so.* librte_gpudev.* librte_graph.so.* librte_gso.so.* librte_hash.so.* librte_ip_frag.so.* librte_ipsec.so.* librte_latencystats.so.* librte_lpm.so.* librte_mbuf.so.* librte_member.so.* librte_mempool.so.* librte_mldev.so.* librte_net.so.* librte_node.* librte_pcapng.so.* librte_pdcp.so.* librte_pdump.so.* librte_pipeline.so.* librte_port.so.* librte_power.so.* librte_rcu.so.* librte_reorder.so.* librte_rib.so.* librte_ring.so.* librte_sched.so.* librte_security.so.* librte_stack.so.* librte_timer.so.* librte_vhost.so.* librte_baseband.*.so.* librte_bus_.*.so.* librte_common_.*.so.* librte_compress_.*.so.* librte_crypto_.* librte_event_.*.so.* librte_mempool_.*.so.* librte_net_.*.so.* librte_raw_.*.so.* librte_regex_.*.so.* librte_vdpa_.*.so.*

%description
DPDK is the Data Plane Development Kit that consists of libraries to
accelerate packet processing workloads running on a wide variety of
CPU architectures.

%description -l pl.UTF-8
DPDK to Data Plane Development Kit, składający się z bibliotek
przyspieszających przetwarzanie pakietów, działających na różnych
architekturach procesorów.

%package devel
Summary:	Header files for DPDK libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek DPDK
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	elfutils-devel
Requires:	jansson-devel
Requires:	libarchive-devel
Requires:	libbpf-devel >= 1.0
Requires:	libbsd-devel
Requires:	libibverbs-devel
Requires:	libibverbs-driver-mana-devel
Requires:	libibverbs-driver-mlx4-devel
Requires:	libibverbs-driver-mlx5-devel
Requires:	libisal-devel
Requires:	libpcap-devel
Requires:	openssl-devel
Requires:	zlib-devel

%description devel
Header files for DPDK libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek DPDK.

%package static
Summary:	Static DPDK libraries
Summary(pl.UTF-8):	Statyczne biblioteki DPDK
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static DPDK libraries.

%description static -l pl.UTF-8
Statyczne biblioteki DPDK.

%package apidocs
Summary:	API documentation for DPDK libraries
Summary(pl.UTF-8):	Dokumentacja API bibliotek DPDK
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for DPDK libraries.

%description apidocs -l pl.UTF-8
Dokumentacja API bibliotek DPDK.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1

%{__sed} -i -e '1s,/usr/bin/env python3,%{__python3},' \
	buildtools/dpdk-cmdline-gen.py \
	usertools/dpdk-{devbind,hugepages,pmdinfo,rss-flows,telemetry,telemetry-exporter}.py \
	examples/ipsec-secgw/test/*.py \
	examples/pipeline/examples/vxlan_table.py

%build
# It builds static libs on its own, --default-libraries=both is not supported.
# Instruction set:
# * -Dplatform=native means building with "-march=native"
# * -Dcpu_instruction_set=native means the same
# * -Dcpu_instruction_set=generic means some modern subset (26.03: -march=corei7 for x86, armv7-a for arm, -mcpu=power8 for ppc, rv64gc for riscv)
# Try to guess instruction set from rpm CFLAGS
%ifarch ppc ppc64
arch=$(echo "%{rpmcflags}" | sed -ne 's/.*-mcpu=\([-0-9a-z_]\+\).*/\1/p')
%else
arch=$(echo "%{rpmcflags}" | sed -ne 's/.*-march=\([-0-9a-z_]\+\).*/\1/p')
%endif
if [ -z "$arch" ]; then
	arch=generic
fi
%meson \
	--default-library=shared \
	--includedir=%{_includedir}/dpdk \
	-Dcpu_instruction_set=$arch \
	-Ddeveloper_mode=disabled \
	-Ddisable_drivers=%{!?with_esmi:power/amd_uncore} \
	%{?with_apidocs:-Denable_docs=true} \
	-Dplatform=generic

# TODO: -Denable_kmods=true

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

install -d $RPM_BUILD_ROOT%{_examplesdir}
%{__mv} $RPM_BUILD_ROOT%{_datadir}/dpdk/examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__rm} $RPM_BUILD_ROOT%{_bindir}/dpdk-test*

%if %{with apidocs}
# cleanup
%{__rm} $RPM_BUILD_ROOT%{_docdir}/dpdk/api/examples.dox
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/dpdk/guides/html/{.doctrees,_sources,.buildinfo,objects.inv}
# many too common names, package just HTML docs, not man pages
%{__rm} -r $RPM_BUILD_ROOT%{_mandir}/man3/*.3
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc MAINTAINERS README
%attr(755,root,root) %{_bindir}/dpdk-cmdline-gen.py
%attr(755,root,root) %{_bindir}/dpdk-devbind.py
%attr(755,root,root) %{_bindir}/dpdk-graph
%attr(755,root,root) %{_bindir}/dpdk-hugepages.py
%attr(755,root,root) %{_bindir}/dpdk-pmdinfo.py
%attr(755,root,root) %{_bindir}/dpdk-proc-info
%attr(755,root,root) %{_bindir}/dpdk-rss-flows.py
%attr(755,root,root) %{_bindir}/dpdk-telemetry.py
%attr(755,root,root) %{_bindir}/dpdk-telemetry-exporter.py
%ifarch %{x8664} aarch64
%attr(755,root,root) %{_bindir}/dpdk-dumpcap
%attr(755,root,root) %{_bindir}/dpdk-pdump
%endif
%{_libdir}/librte_acl.so.*.*
%ghost %{_libdir}/librte_acl.so.%{abi_ver}
%{_libdir}/librte_argparse.so.*.*
%ghost %{_libdir}/librte_argparse.so.%{abi_ver}
%{_libdir}/librte_bbdev.so.*.*
%ghost %{_libdir}/librte_bbdev.so.%{abi_ver}
%{_libdir}/librte_bitratestats.so.*.*
%ghost %{_libdir}/librte_bitratestats.so.%{abi_ver}
%{_libdir}/librte_cfgfile.so.*.*
%ghost %{_libdir}/librte_cfgfile.so.%{abi_ver}
%{_libdir}/librte_cmdline.so.*.*
%ghost %{_libdir}/librte_cmdline.so.%{abi_ver}
%{_libdir}/librte_compressdev.so.*.*
%ghost %{_libdir}/librte_compressdev.so.%{abi_ver}
%{_libdir}/librte_cryptodev.so.*.*
%ghost %{_libdir}/librte_cryptodev.so.%{abi_ver}
%{_libdir}/librte_dispatcher.so.*.*
%ghost %{_libdir}/librte_dispatcher.so.%{abi_ver}
%{_libdir}/librte_distributor.so.*.*
%ghost %{_libdir}/librte_distributor.so.%{abi_ver}
%{_libdir}/librte_dmadev.so.*.*
%ghost %{_libdir}/librte_dmadev.so.%{abi_ver}
%{_libdir}/librte_eal.so.*.*
%ghost %{_libdir}/librte_eal.so.%{abi_ver}
%{_libdir}/librte_efd.so.*.*
%ghost %{_libdir}/librte_efd.so.%{abi_ver}
%{_libdir}/librte_ethdev.so.*.*
%ghost %{_libdir}/librte_ethdev.so.%{abi_ver}
%{_libdir}/librte_eventdev.so.*.*
%ghost %{_libdir}/librte_eventdev.so.%{abi_ver}
%{_libdir}/librte_fib.so.*.*
%ghost %{_libdir}/librte_fib.so.%{abi_ver}
%{_libdir}/librte_gpudev.so.*.*
%ghost %{_libdir}/librte_gpudev.so.%{abi_ver}
%{_libdir}/librte_graph.so.*.*
%ghost %{_libdir}/librte_graph.so.%{abi_ver}
%{_libdir}/librte_gro.so.*.*
%ghost %{_libdir}/librte_gro.so.%{abi_ver}
%{_libdir}/librte_gso.so.*.*
%ghost %{_libdir}/librte_gso.so.%{abi_ver}
%{_libdir}/librte_hash.so.*.*
%ghost %{_libdir}/librte_hash.so.%{abi_ver}
%{_libdir}/librte_ip_frag.so.*.*
%ghost %{_libdir}/librte_ip_frag.so.%{abi_ver}
%{_libdir}/librte_ipsec.so.*.*
%ghost %{_libdir}/librte_ipsec.so.%{abi_ver}
%{_libdir}/librte_jobstats.so.*.*
%ghost %{_libdir}/librte_jobstats.so.%{abi_ver}
%{_libdir}/librte_kvargs.so.*.*
%ghost %{_libdir}/librte_kvargs.so.%{abi_ver}
%{_libdir}/librte_latencystats.so.*.*
%ghost %{_libdir}/librte_latencystats.so.%{abi_ver}
%{_libdir}/librte_log.so.*.*
%ghost %{_libdir}/librte_log.so.%{abi_ver}
%{_libdir}/librte_lpm.so.*.*
%ghost %{_libdir}/librte_lpm.so.%{abi_ver}
%{_libdir}/librte_mbuf.so.*.*
%ghost %{_libdir}/librte_mbuf.so.%{abi_ver}
%{_libdir}/librte_member.so.*.*
%ghost %{_libdir}/librte_member.so.%{abi_ver}
%{_libdir}/librte_mempool.so.*.*
%ghost %{_libdir}/librte_mempool.so.%{abi_ver}
%{_libdir}/librte_meter.so.*.*
%ghost %{_libdir}/librte_meter.so.%{abi_ver}
%{_libdir}/librte_metrics.so.*.*
%ghost %{_libdir}/librte_metrics.so.%{abi_ver}
%{_libdir}/librte_mldev.so.*.*
%ghost %{_libdir}/librte_mldev.so.%{abi_ver}
%{_libdir}/librte_net.so.*.*
%ghost %{_libdir}/librte_net.so.%{abi_ver}
%{_libdir}/librte_node.so.*.*
%ghost %{_libdir}/librte_node.so.%{abi_ver}
%{_libdir}/librte_pcapng.so.*.*
%ghost %{_libdir}/librte_pcapng.so.%{abi_ver}
%{_libdir}/librte_pci.so.*.*
%ghost %{_libdir}/librte_pci.so.%{abi_ver}
%{_libdir}/librte_pdcp.so.*.*
%ghost %{_libdir}/librte_pdcp.so.%{abi_ver}
%{_libdir}/librte_pipeline.so.*.*
%ghost %{_libdir}/librte_pipeline.so.%{abi_ver}
%{_libdir}/librte_pmu.so.*.*
%ghost %{_libdir}/librte_pmu.so.%{abi_ver}
%{_libdir}/librte_port.so.*.*
%ghost %{_libdir}/librte_port.so.%{abi_ver}
%{_libdir}/librte_power.so.*.*
%ghost %{_libdir}/librte_power.so.%{abi_ver}
%{_libdir}/librte_rawdev.so.*.*
%ghost %{_libdir}/librte_rawdev.so.%{abi_ver}
%{_libdir}/librte_rcu.so.*.*
%ghost %{_libdir}/librte_rcu.so.%{abi_ver}
%{_libdir}/librte_regexdev.so.*.*
%ghost %{_libdir}/librte_regexdev.so.%{abi_ver}
%{_libdir}/librte_reorder.so.*.*
%ghost %{_libdir}/librte_reorder.so.%{abi_ver}
%{_libdir}/librte_rib.so.*.*
%ghost %{_libdir}/librte_rib.so.%{abi_ver}
%{_libdir}/librte_ring.so.*.*
%ghost %{_libdir}/librte_ring.so.%{abi_ver}
%{_libdir}/librte_sched.so.*.*
%ghost %{_libdir}/librte_sched.so.%{abi_ver}
%{_libdir}/librte_security.so.*.*
%ghost %{_libdir}/librte_security.so.%{abi_ver}
%{_libdir}/librte_stack.so.*.*
%ghost %{_libdir}/librte_stack.so.%{abi_ver}
%{_libdir}/librte_table.so.*.*
%ghost %{_libdir}/librte_table.so.%{abi_ver}
%{_libdir}/librte_telemetry.so.*.*
%ghost %{_libdir}/librte_telemetry.so.%{abi_ver}
%{_libdir}/librte_timer.so.*.*
%ghost %{_libdir}/librte_timer.so.%{abi_ver}
%{_libdir}/librte_vhost.so.*.*
%ghost %{_libdir}/librte_vhost.so.%{abi_ver}
%ifarch %{x8664} aarch64
%{_libdir}/librte_bpf.so.*.*
%ghost %{_libdir}/librte_bpf.so.%{abi_ver}
%{_libdir}/librte_pdump.so.*.*
%ghost %{_libdir}/librte_pdump.so.%{abi_ver}
%endif
%dir %{_libdir}/dpdk
%dir %{_libdir}/dpdk/pmds-%{lib_ver}
%{_libdir}/dpdk/pmds-%{lib_ver}/librte_baseband_*.so*
%{_libdir}/dpdk/pmds-%{lib_ver}/librte_bus_*.so*
%{_libdir}/dpdk/pmds-%{lib_ver}/librte_common_*.so*
%{_libdir}/dpdk/pmds-%{lib_ver}/librte_compress_*.so*
%{_libdir}/dpdk/pmds-%{lib_ver}/librte_crypto_*.so*
%{_libdir}/dpdk/pmds-%{lib_ver}/librte_dma_*.so*
%{_libdir}/dpdk/pmds-%{lib_ver}/librte_event_*.so*
%{_libdir}/dpdk/pmds-%{lib_ver}/librte_mempool_*.so*
%ifarch %{x8664} aarch64 ppc64
%{_libdir}/dpdk/pmds-%{lib_ver}/librte_ml_cnxk.so*
%endif
%{_libdir}/dpdk/pmds-%{lib_ver}/librte_net_*.so*
%{_libdir}/dpdk/pmds-%{lib_ver}/librte_power_*.so*
%{_libdir}/dpdk/pmds-%{lib_ver}/librte_raw_*.so*
%{_libdir}/dpdk/pmds-%{lib_ver}/librte_regex_*.so*
%{_libdir}/dpdk/pmds-%{lib_ver}/librte_vdpa_*.so*
# symlinks
%{_libdir}/librte_baseband_*.so.*.*
%ghost %{_libdir}/librte_baseband_*.so.%{abi_ver}
%{_libdir}/librte_bus_*.so.*.*
%ghost %{_libdir}/librte_bus_*.so.%{abi_ver}
%{_libdir}/librte_common_*.so.*.*
%ghost %{_libdir}/librte_common_*.so.%{abi_ver}
%{_libdir}/librte_compress_*.so.*.*
%ghost %{_libdir}/librte_compress_*.so.%{abi_ver}
%{_libdir}/librte_crypto_*.so.*.*
%ghost %{_libdir}/librte_crypto_*.so.%{abi_ver}
%{_libdir}/librte_dma_*.so.*.*
%ghost %{_libdir}/librte_dma_*.so.%{abi_ver}
%{_libdir}/librte_event_*.so.*.*
%ghost %{_libdir}/librte_event_*.so.%{abi_ver}
%{_libdir}/librte_mempool_*.so.*.*
%ghost %{_libdir}/librte_mempool_*.so.%{abi_ver}
%ifarch %{x8664} aarch64 ppc64
%{_libdir}/librte_ml_cnxk.so.*.*
%ghost %{_libdir}/librte_ml_cnxk.so.%{abi_ver}
%endif
%{_libdir}/librte_net_*.so.*.*
%ghost %{_libdir}/librte_net_*.so.%{abi_ver}
%{_libdir}/librte_power_*.so.*.*
%ghost %{_libdir}/librte_power_*.so.%{abi_ver}
%{_libdir}/librte_raw_*.so.*.*
%ghost %{_libdir}/librte_raw_*.so.%{abi_ver}
%{_libdir}/librte_regex_*.so.*.*
%ghost %{_libdir}/librte_regex_*.so.%{abi_ver}
%{_libdir}/librte_vdpa_*.so.*.*
%ghost %{_libdir}/librte_vdpa_*.so.%{abi_ver}
%dir %{_datadir}/dpdk
%{_datadir}/dpdk/telemetry-endpoints

%files devel
%defattr(644,root,root,755)
%{_libdir}/librte_acl.so
%{_libdir}/librte_argparse.so
%{_libdir}/librte_bbdev.so
%{_libdir}/librte_bitratestats.so
%{_libdir}/librte_cfgfile.so
%{_libdir}/librte_cmdline.so
%{_libdir}/librte_compressdev.so
%{_libdir}/librte_cryptodev.so
%{_libdir}/librte_dispatcher.so
%{_libdir}/librte_distributor.so
%{_libdir}/librte_dmadev.so
%{_libdir}/librte_eal.so
%{_libdir}/librte_efd.so
%{_libdir}/librte_ethdev.so
%{_libdir}/librte_eventdev.so
%{_libdir}/librte_fib.so
%{_libdir}/librte_gpudev.so
%{_libdir}/librte_graph.so
%{_libdir}/librte_gro.so
%{_libdir}/librte_gso.so
%{_libdir}/librte_hash.so
%{_libdir}/librte_ip_frag.so
%{_libdir}/librte_ipsec.so
%{_libdir}/librte_jobstats.so
%{_libdir}/librte_kvargs.so
%{_libdir}/librte_latencystats.so
%{_libdir}/librte_log.so
%{_libdir}/librte_lpm.so
%{_libdir}/librte_mbuf.so
%{_libdir}/librte_member.so
%{_libdir}/librte_mempool.so
%{_libdir}/librte_meter.so
%{_libdir}/librte_metrics.so
%{_libdir}/librte_mldev.so
%{_libdir}/librte_net.so
%{_libdir}/librte_node.so
%{_libdir}/librte_pcapng.so
%{_libdir}/librte_pci.so
%{_libdir}/librte_pdcp.so
%{_libdir}/librte_pipeline.so
%{_libdir}/librte_pmu.so
%{_libdir}/librte_port.so
%{_libdir}/librte_power.so
%{_libdir}/librte_rawdev.so
%{_libdir}/librte_rcu.so
%{_libdir}/librte_regexdev.so
%{_libdir}/librte_reorder.so
%{_libdir}/librte_rib.so
%{_libdir}/librte_ring.so
%{_libdir}/librte_sched.so
%{_libdir}/librte_security.so
%{_libdir}/librte_stack.so
%{_libdir}/librte_table.so
%{_libdir}/librte_telemetry.so
%{_libdir}/librte_timer.so
%{_libdir}/librte_vhost.so
%ifarch %{x8664} aarch64
%{_libdir}/librte_bpf.so
%{_libdir}/librte_pdump.so
%endif
# symlinks to subdir
%{_libdir}/librte_baseband_*.so
%{_libdir}/librte_bus_*.so
%{_libdir}/librte_common_*.so
%{_libdir}/librte_compress_*.so
%{_libdir}/librte_crypto_*.so
%{_libdir}/librte_dma_*.so
%{_libdir}/librte_event_*.so
%{_libdir}/librte_mempool_*.so
%ifarch %{x8664} aarch64 ppc64
%{_libdir}/librte_ml_cnxk.so
%endif
%{_libdir}/librte_net_*.so
%{_libdir}/librte_raw_*.so
%{_libdir}/librte_power_*.so
%{_libdir}/librte_regex_*.so
%{_libdir}/librte_vdpa_*.so
%{_includedir}/dpdk
%{_pkgconfigdir}/libdpdk.pc
%{_pkgconfigdir}/libdpdk-libs.pc
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/librte_acl.a
%{_libdir}/librte_argparse.a
%{_libdir}/librte_bbdev.a
%{_libdir}/librte_bitratestats.a
%{_libdir}/librte_cfgfile.a
%{_libdir}/librte_cmdline.a
%{_libdir}/librte_compressdev.a
%{_libdir}/librte_cryptodev.a
%{_libdir}/librte_dispatcher.a
%{_libdir}/librte_distributor.a
%{_libdir}/librte_dmadev.a
%{_libdir}/librte_eal.a
%{_libdir}/librte_efd.a
%{_libdir}/librte_ethdev.a
%{_libdir}/librte_eventdev.a
%{_libdir}/librte_fib.a
%{_libdir}/librte_gpudev.a
%{_libdir}/librte_graph.a
%{_libdir}/librte_gro.a
%{_libdir}/librte_gso.a
%{_libdir}/librte_hash.a
%{_libdir}/librte_ip_frag.a
%{_libdir}/librte_ipsec.a
%{_libdir}/librte_jobstats.a
%{_libdir}/librte_kvargs.a
%{_libdir}/librte_latencystats.a
%{_libdir}/librte_log.a
%{_libdir}/librte_lpm.a
%{_libdir}/librte_mbuf.a
%{_libdir}/librte_member.a
%{_libdir}/librte_mempool.a
%{_libdir}/librte_meter.a
%{_libdir}/librte_metrics.a
%{_libdir}/librte_mldev.a
%{_libdir}/librte_net.a
%{_libdir}/librte_node.a
%{_libdir}/librte_pcapng.a
%{_libdir}/librte_pci.a
%{_libdir}/librte_pdcp.a
%{_libdir}/librte_pipeline.a
%{_libdir}/librte_pmu.a
%{_libdir}/librte_port.a
%{_libdir}/librte_power.a
%{_libdir}/librte_power_acpi.a
%{_libdir}/librte_power_amd_pstate.a
%if %{with esmi}
%{_libdir}/librte_power_amd_uncore.a
%endif
%{_libdir}/librte_power_cppc.a
%{_libdir}/librte_power_intel_pstate.a
%{_libdir}/librte_power_intel_uncore.a
%{_libdir}/librte_power_kvm_vm.a
%{_libdir}/librte_rawdev.a
%{_libdir}/librte_rcu.a
%{_libdir}/librte_regexdev.a
%{_libdir}/librte_reorder.a
%{_libdir}/librte_rib.a
%{_libdir}/librte_ring.a
%{_libdir}/librte_sched.a
%{_libdir}/librte_security.a
%{_libdir}/librte_stack.a
%{_libdir}/librte_table.a
%{_libdir}/librte_telemetry.a
%{_libdir}/librte_timer.a
%{_libdir}/librte_vhost.a
%ifarch %{x8664} aarch64
%{_libdir}/librte_bpf.a
%{_libdir}/librte_pdump.a
%endif
# drivers
%{_libdir}/librte_baseband_*.a
%{_libdir}/librte_bus_*.a
%{_libdir}/librte_common_*.a
%{_libdir}/librte_compress_*.a
%{_libdir}/librte_crypto_*.a
%{_libdir}/librte_dma_*.a
%{_libdir}/librte_event_*.a
%{_libdir}/librte_mempool_*.a
%ifarch %{x8664} aarch64 ppc64
%{_libdir}/librte_ml_cnxk.a
%endif
%{_libdir}/librte_net_*.a
%{_libdir}/librte_raw_*.a
%{_libdir}/librte_regex_*.a
%{_libdir}/librte_vdpa_*.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_docdir}/dpdk
%endif
