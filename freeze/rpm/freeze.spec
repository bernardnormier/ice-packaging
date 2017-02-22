# **********************************************************************
#
# Copyright (c) 2003-2017 ZeroC, Inc. All rights reserved.
#
# **********************************************************************

%define expatdevel expat-devel
%define bzip2devel bzip2-devel

%if "%{dist}" == ".sles12"
  %define expatdevel libexpat-devel
  %define bzip2devel libbz2-devel
%endif

%if "%{_prefix}" == "/usr"
%define runpath embedded_runpath=no
%else
%define runpath embedded_runpath_prefix=%{_prefix}
%endif

%define makebuildopts CONFIGS="shared" OPTIMIZE=yes V=1 %{runpath} %{?_smp_mflags}
%define makeinstallopts CONFIGS="shared" OPTIMIZE=yes V=1 %{runpath} DESTDIR=$RPM_BUILD_ROOT prefix=%{_prefix} install_bindir=%{_bindir} install_libdir=%{_libdir} install_includedir=%{_includedir} install_mandir=%{_mandir}

Name: %{?nameprefix}freeze
Version: 3.7a4
Summary: Persistent storage for Ice objects
Release: 1%{?dist}
%if "%{?ice_license}"
License: %{ice_license}
%else
License: GPLv2
%endif
Vendor: ZeroC, Inc.
URL: https://zeroc.com/
Source: https://github.com/zeroc-ice/freeze/archive/v3.7.0-alpha4/%{name}-%{version}.tar.gz
BuildRequires: mcpp-devel, %{bzip2devel}, %{expatdevel}

#
# Enable debug package except if it's already enabled
#
%if %{!?_enable_debug_packages:1}%{?_enable_debug_packages:0}
%debug_package
%endif

#
# libfreezeM.m-c++ package
#
%package -n lib%{?nameprefix}freeze3.7-c++
Summary: Freeze for C++ run-time library.
Group: System Environment/Libraries
Requires: lib%{?nameprefix}ice3.7-c++%{?_isa} = %{version}-%{release}
%description -n lib%{?nameprefix}freeze3.7-c++
This package contains the C++ run-time library for the Freeze service.

Freeze provides persistent storage for Ice objects.

#
# libfreeze-c++-devel package
#
%package -n lib%{?nameprefix}freeze-c++-devel
Summary: Libraries and headers for developing Freeze applications in C++.
Group: Development/Tools
Obsoletes: ice-c++-devel < 3.6
Requires: lib%{?nameprefix}freeze3.7-c++%{?_isa} = %{version}-%{release}
Requires: %{?nameprefix}freeze-compilers(x86-64) = %{version}-%{release}
%description -n lib%{?nameprefix}freeze-c++-devel
This package contains the library and header files needed for developing
Freeze applications in C++.

Freeze provides persistent storage for Ice objects.

#
# freeze-compilers package
#
%package -n %{?nameprefix}freeze-compilers
Summary: Slice compilers for developing Freeze applications
Group: Development/Tools
Requires: %{?nameprefix}ice-slice = %{version}-%{release}
%description -n %{?nameprefix}freeze-compilers
This package contains Slice compilers for developing Freeze applications.

Freeze provides persistent storage for Ice objects.

#
# freeze-utils package
#
%package -n %{?nameprefix}freeze-utils
Summary: Freeze utilities
Group: Applications/System
Obsoletes: ice-utils < 3.6
Requires: lib%{?nameprefix}freeze3.7-c++%{?_isa} = %{version}-%{release}
%description -n %{?nameprefix}freeze-utils
This package contains Freeze utilities.

Freeze provides persistent storage for Ice objects.

%prep
%setup -q -n %{name}-%{version}

%build
# recommended flags for optimized hardened build
export CXXFLAGS="%{optflags}"
export LDFLAGS="%{?__global_ldflags}"

make -C ice/cpp %{makebuildopts} IceXML
make -C cpp %{makebuildopts} srcs 

%install
make %{makeinstallopts} install

#
# libfreezeM.m-c++ package
#
%files -n lib%{?nameprefix}freeze3.7-c++
%{_libdir}/libFreeze.so.*
%{_defaultdocdir}/lib%{?nameprefix}freeze3.7-c++-%{version}
%post -n lib%{?nameprefix}freeze3.7-c++ -p /sbin/ldconfig
%postun -n lib%{?nameprefix}freeze3.7-c++
/sbin/ldconfig
exit 0

#
# libfreeze-c++-devel package
#
%files -n lib%{?nameprefix}freeze-c++-devel
%{_libdir}/libFreeze.so
%{_includedir}/Freeze
%{_defaultdocdir}/lib%{?nameprefix}freeze-c++-devel-%{version}

#
# freeze-compilers package
#
%files -n %{?nameprefix}freeze-compilers
%{_bindir}/slice2freeze
%{_mandir}/man1/slice2freeze.1*
%{_bindir}/slice2freezej
%{_mandir}/man1/slice2freezej.1*
%{_defaultdocdir}/%{?nameprefix}freeze-compilers-%{version}

#
# freeze-utils package
#
%files -n %{?nameprefix}freeze-utils
%{_bindir}/dumpdb
%{_mandir}/man1/dumpdb.1*
%{_bindir}/transformdb
%{_mandir}/man1/transformdb.1*
%{_defaultdocdir}/%{?nameprefix}freeze-utils-%{version}


%changelog
* Tue Feb 21 2017 Bernard Normier <bernard@zeroc.com> 3.7.0-alpha4
- Initial package
