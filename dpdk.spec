# TODO:
# - kernel part (igb_uio and kni modules)
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
#   https://github.com/Linaro/uadk
# - cuda for drivers/gpu/cuda
# - pkgconfig(netcope-common) for driver/net/nfb
#   https://www.netcope.com/en/company/community-support/dpdk-libsze2 or https://www.liberouter.org/repo/dcpro/base/ - x86_64 only
# - pkgconfig(libsze2) for drivers/net/szedata2
#   https://www.netcope.com/en/company/community-support/dpdk-libsze2 - x86_64 only
#   some old versions at https://homeproj.cesnet.cz/rpm/liberouter/{devel,stable}/SRPMS/
#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	rte_kni		# RTE_KNI library (deprecated)

%ifnarch %{x8664} aarch64 ppc64
%undefine	with_rte_kni
%endif
Summary:	Data Plane Development Kit libraries
Summary(pl.UTF-8):	Biblioteki Data Plane Development Kit
Name:		dpdk
Version:	23.11
Release:	1
License:	BSD (libraries and drivers), GPL v2 (kernel components)
Group:		Libraries
Source0:	https://fast.dpdk.org/rel/%{name}-%{version}.tar.xz
# Source0-md5:	896c09f5b45b452bd77287994650b916
Patch0:		%{name}-time.patch
URL:		https://www.dpdk.org/
# pkgconfig(libelf)
BuildRequires:	elfutils-devel
# C11
BuildRequires:	gcc >= 6:4.7
%ifarch aarch64
BuildRequires:	gcc >= 6:4.8.6
%endif
BuildRequires:	jansson-devel
BuildRequires:	libarchive-devel
BuildRequires:	libbpf-devel
BuildRequires:	libbsd-devel
BuildRequires:	libfdt-devel
BuildRequires:	libibverbs-devel
BuildRequires:	libibverbs-driver-mana-devel
BuildRequires:	libibverbs-driver-mlx4-devel
BuildRequires:	libibverbs-driver-mlx5-devel
BuildRequires:	libisal-devel
BuildRequires:	libpcap-devel
BuildRequires:	libxdp-devel
# vduse etc.
BuildRequires:	linux-libc-headers >= 7:5.15
BuildRequires:	meson >= 0.53.2
BuildRequires:	ninja >= 1.5
BuildRequires:	numactl-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 3
BuildRequires:	python3-elftools
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
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

%define		abi_ver		24
%define		lib_ver		%{abi_ver}.0

# non-function symbols per_lcore__lcore_id, per_lcore__rte_errno, per_lcore__thread_id, per_lcore_dpaa_io, per_lcore__dpaa2_io, per_lcore_held_bufs, per_lcore_dpaa2_held_bufs
%define		skip_post_check_so	librte_acl.so.* librte_bbdev.so.* librte_bpf.so.* librte_compressdev.so.* librte_cryptodev.so.* librte_dispatcher.so.* librte_distributor.so.* librte_dma_dpaa2.so.* librte_dma_ioat.so.* librte_dmadev.so.* librte_efd.so.* librte_eventdev.so.* librte_ethdev.so.* librte_fib.so.* librte_gpudev.* librte_graph.so.* librte_gso.so.* librte_hash.so.* librte_ip_frag.so.* librte_ipsec.so.* librte_kni.so.* librte_latencystats.so.* librte_lpm.so.* librte_mbuf.so.* librte_member.so.* librte_mempool.so.* librte_mldev.so.* librte_net.so.* librte_node.* librte_pcapng.so.* librte_pdcp.so.* librte_pdump.so.* librte_pipeline.so.* librte_port.so.* librte_power.so.* librte_rcu.so.* librte_reorder.so.* librte_rib.so.* librte_ring.so.* librte_sched.so.* librte_security.so.* librte_stack.so.* librte_timer.so.* librte_vhost.so.* librte_baseband.*.so.* librte_bus_.*.so.* librte_common_.*.so.* librte_compress_.*.so.* librte_crypto_.* librte_event_.*.so.* librte_mempool_.*.so.* librte_net_.*.so.* librte_raw_.*.so.* librte_regex_.*.so.* librte_vdpa_.*.so.*

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
Requires:	libbsd-devel
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
%patch0 -p1

%{__sed} -i -e '1s,/usr/bin/env python3,%{__python3},' \
	buildtools/dpdk-cmdline-gen.py \
	usertools/dpdk-{devbind,hugepages,pmdinfo,rss-flows,telemetry}.py \
	examples/ipsec-secgw/test/*.py \
	examples/pipeline/examples/vxlan_table.py

%build
# it builds static libs on its own, --default-libraries=both is not supported
%meson build \
	--default-library=shared \
	--includedir=%{_includedir}/dpdk \
	-Ddisable_libs=%{!?with_rte_kni:kni} \
	%{?with_apidocs:-Denable_docs=true} \
	-Dplatform=generic

# TODO: -Denable_kmods=true

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

install -d $RPM_BUILD_ROOT%{_examplesdir}
%{__mv} $RPM_BUILD_ROOT%{_datadir}/dpdk/examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__rm} $RPM_BUILD_ROOT%{_bindir}/dpdk-test*

%if %{with apidocs}
# cleanup
%{__rm} $RPM_BUILD_ROOT%{_docdir}/dpdk/examples.dox
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/dpdk/html/{.doctrees,_sources,.buildinfo,objects.inv}
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
%attr(755,root,root) %{_bindir}/dpdk-dumpcap
%attr(755,root,root) %{_bindir}/dpdk-graph
%attr(755,root,root) %{_bindir}/dpdk-hugepages.py
%attr(755,root,root) %{_bindir}/dpdk-pdump
%attr(755,root,root) %{_bindir}/dpdk-pmdinfo.py
%attr(755,root,root) %{_bindir}/dpdk-proc-info
%attr(755,root,root) %{_bindir}/dpdk-rss-flows.py
%attr(755,root,root) %{_bindir}/dpdk-telemetry.py
%attr(755,root,root) %{_libdir}/librte_acl.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_acl.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_bbdev.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_bbdev.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_bitratestats.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_bitratestats.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_bpf.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_bpf.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_cfgfile.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_cfgfile.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_cmdline.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_cmdline.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_compressdev.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_compressdev.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_cryptodev.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_cryptodev.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_dispatcher.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_dispatcher.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_distributor.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_distributor.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_dmadev.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_dmadev.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_eal.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_eal.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_efd.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_efd.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_ethdev.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_ethdev.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_eventdev.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_eventdev.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_fib.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_fib.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_gpudev.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_gpudev.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_graph.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_graph.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_gro.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_gro.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_gso.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_gso.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_hash.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_hash.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_ip_frag.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_ip_frag.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_ipsec.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_ipsec.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_jobstats.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_jobstats.so.%{abi_ver}
%if %{with rte_kni}
%attr(755,root,root) %{_libdir}/librte_kni.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_kni.so.%{abi_ver}
%endif
%attr(755,root,root) %{_libdir}/librte_kvargs.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_kvargs.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_latencystats.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_latencystats.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_log.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_log.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_lpm.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_lpm.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_mbuf.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_mbuf.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_member.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_member.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_mempool.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_mempool.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_meter.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_meter.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_metrics.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_metrics.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_mldev.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_mldev.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_net.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_net.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_node.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_node.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_pcapng.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_pcapng.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_pci.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_pci.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_pdcp.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_pdcp.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_pdump.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_pdump.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_pipeline.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_pipeline.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_port.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_port.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_power.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_power.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_rawdev.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_rawdev.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_rcu.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_rcu.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_regexdev.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_regexdev.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_reorder.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_reorder.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_rib.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_rib.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_ring.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_ring.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_sched.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_sched.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_security.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_security.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_stack.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_stack.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_table.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_table.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_telemetry.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_telemetry.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_timer.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_timer.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_vhost.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_vhost.so.%{abi_ver}
%dir %{_libdir}/dpdk
%dir %{_libdir}/dpdk/pmds-%{lib_ver}
%attr(755,root,root) %{_libdir}/dpdk/pmds-%{lib_ver}/librte_baseband_*.so*
%attr(755,root,root) %{_libdir}/dpdk/pmds-%{lib_ver}/librte_bus_*.so*
%attr(755,root,root) %{_libdir}/dpdk/pmds-%{lib_ver}/librte_common_*.so*
%attr(755,root,root) %{_libdir}/dpdk/pmds-%{lib_ver}/librte_compress_*.so*
%attr(755,root,root) %{_libdir}/dpdk/pmds-%{lib_ver}/librte_crypto_*.so*
%attr(755,root,root) %{_libdir}/dpdk/pmds-%{lib_ver}/librte_dma_*.so*
%attr(755,root,root) %{_libdir}/dpdk/pmds-%{lib_ver}/librte_event_*.so*
%attr(755,root,root) %{_libdir}/dpdk/pmds-%{lib_ver}/librte_mempool_*.so*
%ifarch %{x8664} aarch64 ppc64
%attr(755,root,root) %{_libdir}/dpdk/pmds-%{lib_ver}/librte_ml_cnxk.so*
%endif
%attr(755,root,root) %{_libdir}/dpdk/pmds-%{lib_ver}/librte_net_*.so*
%attr(755,root,root) %{_libdir}/dpdk/pmds-%{lib_ver}/librte_raw_*.so*
%attr(755,root,root) %{_libdir}/dpdk/pmds-%{lib_ver}/librte_regex_*.so*
%attr(755,root,root) %{_libdir}/dpdk/pmds-%{lib_ver}/librte_vdpa_*.so*
# symlinks
%attr(755,root,root) %{_libdir}/librte_baseband_*.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_baseband_*.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_bus_*.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_bus_*.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_common_*.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_common_*.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_compress_*.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_compress_*.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_crypto_*.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_crypto_*.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_dma_*.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_dma_*.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_event_*.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_event_*.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_mempool_*.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_mempool_*.so.%{abi_ver}
%ifarch %{x8664} aarch64 ppc64
%attr(755,root,root) %{_libdir}/librte_ml_cnxk.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_ml_cnxk.so.%{abi_ver}
%endif
%attr(755,root,root) %{_libdir}/librte_net_*.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_net_*.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_raw_*.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_raw_*.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_regex_*.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_regex_*.so.%{abi_ver}
%attr(755,root,root) %{_libdir}/librte_vdpa_*.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librte_vdpa_*.so.%{abi_ver}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/librte_acl.so
%attr(755,root,root) %{_libdir}/librte_bbdev.so
%attr(755,root,root) %{_libdir}/librte_bitratestats.so
%attr(755,root,root) %{_libdir}/librte_bpf.so
%attr(755,root,root) %{_libdir}/librte_cfgfile.so
%attr(755,root,root) %{_libdir}/librte_cmdline.so
%attr(755,root,root) %{_libdir}/librte_compressdev.so
%attr(755,root,root) %{_libdir}/librte_cryptodev.so
%attr(755,root,root) %{_libdir}/librte_dispatcher.so
%attr(755,root,root) %{_libdir}/librte_distributor.so
%attr(755,root,root) %{_libdir}/librte_dmadev.so
%attr(755,root,root) %{_libdir}/librte_eal.so
%attr(755,root,root) %{_libdir}/librte_efd.so
%attr(755,root,root) %{_libdir}/librte_ethdev.so
%attr(755,root,root) %{_libdir}/librte_eventdev.so
%attr(755,root,root) %{_libdir}/librte_fib.so
%attr(755,root,root) %{_libdir}/librte_gpudev.so
%attr(755,root,root) %{_libdir}/librte_graph.so
%attr(755,root,root) %{_libdir}/librte_gro.so
%attr(755,root,root) %{_libdir}/librte_gso.so
%attr(755,root,root) %{_libdir}/librte_hash.so
%attr(755,root,root) %{_libdir}/librte_ip_frag.so
%attr(755,root,root) %{_libdir}/librte_ipsec.so
%attr(755,root,root) %{_libdir}/librte_jobstats.so
%if %{with rte_kni}
%attr(755,root,root) %{_libdir}/librte_kni.so
%endif
%attr(755,root,root) %{_libdir}/librte_kvargs.so
%attr(755,root,root) %{_libdir}/librte_latencystats.so
%attr(755,root,root) %{_libdir}/librte_log.so
%attr(755,root,root) %{_libdir}/librte_lpm.so
%attr(755,root,root) %{_libdir}/librte_mbuf.so
%attr(755,root,root) %{_libdir}/librte_member.so
%attr(755,root,root) %{_libdir}/librte_mempool.so
%attr(755,root,root) %{_libdir}/librte_meter.so
%attr(755,root,root) %{_libdir}/librte_metrics.so
%attr(755,root,root) %{_libdir}/librte_mldev.so
%attr(755,root,root) %{_libdir}/librte_net.so
%attr(755,root,root) %{_libdir}/librte_node.so
%attr(755,root,root) %{_libdir}/librte_pcapng.so
%attr(755,root,root) %{_libdir}/librte_pci.so
%attr(755,root,root) %{_libdir}/librte_pdcp.so
%attr(755,root,root) %{_libdir}/librte_pdump.so
%attr(755,root,root) %{_libdir}/librte_pipeline.so
%attr(755,root,root) %{_libdir}/librte_port.so
%attr(755,root,root) %{_libdir}/librte_power.so
%attr(755,root,root) %{_libdir}/librte_rawdev.so
%attr(755,root,root) %{_libdir}/librte_rcu.so
%attr(755,root,root) %{_libdir}/librte_regexdev.so
%attr(755,root,root) %{_libdir}/librte_reorder.so
%attr(755,root,root) %{_libdir}/librte_rib.so
%attr(755,root,root) %{_libdir}/librte_ring.so
%attr(755,root,root) %{_libdir}/librte_sched.so
%attr(755,root,root) %{_libdir}/librte_security.so
%attr(755,root,root) %{_libdir}/librte_stack.so
%attr(755,root,root) %{_libdir}/librte_table.so
%attr(755,root,root) %{_libdir}/librte_telemetry.so
%attr(755,root,root) %{_libdir}/librte_timer.so
%attr(755,root,root) %{_libdir}/librte_vhost.so
# symlinks to subdir
%attr(755,root,root) %{_libdir}/librte_baseband_*.so
%attr(755,root,root) %{_libdir}/librte_bus_*.so
%attr(755,root,root) %{_libdir}/librte_common_*.so
%attr(755,root,root) %{_libdir}/librte_compress_*.so
%attr(755,root,root) %{_libdir}/librte_crypto_*.so
%attr(755,root,root) %{_libdir}/librte_dma_*.so
%attr(755,root,root) %{_libdir}/librte_event_*.so
%attr(755,root,root) %{_libdir}/librte_mempool_*.so
%ifarch %{x8664} aarch64 ppc64
%attr(755,root,root) %{_libdir}/librte_ml_cnxk.so
%endif
%attr(755,root,root) %{_libdir}/librte_net_*.so
%attr(755,root,root) %{_libdir}/librte_raw_*.so
%attr(755,root,root) %{_libdir}/librte_regex_*.so
%attr(755,root,root) %{_libdir}/librte_vdpa_*.so
%{_includedir}/dpdk
%{_pkgconfigdir}/libdpdk.pc
%{_pkgconfigdir}/libdpdk-libs.pc
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/librte_acl.a
%{_libdir}/librte_bbdev.a
%{_libdir}/librte_bitratestats.a
%{_libdir}/librte_bpf.a
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
%if %{with rte_kni}
%{_libdir}/librte_kni.a
%endif
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
%{_libdir}/librte_pdump.a
%{_libdir}/librte_pipeline.a
%{_libdir}/librte_port.a
%{_libdir}/librte_power.a
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
