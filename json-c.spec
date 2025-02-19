# (tpg) reduce bloat by excluding cmake requires on devel packages
%global __requires_exclude ^cmake.*$

# fontconfig uses json-c, wine uses fontconfig
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif

# As of 0.14 and 0.15:
# json_object.c:1338:68: error: dereferencing type-punned pointer might break strict-aliasing rules [-Werror=strict-aliasing]
# json_object.c:1408:72: error: dereferencing type-punned pointer might break strict-aliasing rules [-Werror=strict-aliasing]
# json_object.c:1417:72: error: dereferencing type-punned pointer might break strict-aliasing rules [-Werror=strict-aliasing]
# https://github.com/json-c/json-c/issues/676
%global optflags %{optflags} -fno-strict-aliasing
%global build_ldflags %{build_ldflags} -Wl,--undefined-version
 
%define oldmaj 0
%define major 5
%define oldlibname %mklibname %{name}
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d
%define oldlib32name %mklib32name %{name} 5
%define lib32name %mklib32name %{name}
%define dev32name %mklib32name %{name} -d
%bcond_with crosscompile

Summary:	JSON implementation in C
Name:		json-c
Version:	0.18
Release:	1
Group:		System/Libraries
License:	MIT
Url:		https://github.com/json-c/json-c/wiki
Source0:	https://s3.amazonaws.com/json-c_releases/releases/%{name}-%{version}.tar.gz
BuildRequires:	cmake
BuildRequires:	ninja

%description
JSON-C implements a reference counting object model that allows you to
easily construct JSON objects in C, output them as JSON formatted
strings and parse JSON formatted strings back into the C
representation of JSON objects.

%package -n %{libname}
Summary:	JSON implementation in C
Group:		System/Libraries
%rename %{oldlibname}

%description -n %{libname}
JSON-C implements a reference counting object model that allows you to
easily construct JSON objects in C, output them as JSON formatted
strings and parse JSON formatted strings back into the C
representation of JSON objects.

%package -n %{devname}
Summary:	Development headers and libraries for %{name}
Group:		Development/C
Requires:	%{libname} >= %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}json-devel < 0.11-2

%description -n %{devname}
JSON-C implements a reference counting object model that allows you to
easily construct JSON objects in C, output them as JSON formatted
strings and parse JSON formatted strings back into the C
representation of JSON objects.

%if %{with compat32}
%package -n %{lib32name}
Summary:	JSON implementation in C (32-bit)
Group:		System/Libraries
BuildRequires:	libc6
Requires:	libc6
%rename %{oldlib32name}

%description -n %{lib32name}
JSON-C implements a reference counting object model that allows you to
easily construct JSON objects in C, output them as JSON formatted
strings and parse JSON formatted strings back into the C
representation of JSON objects.

%package -n %{dev32name}
Summary:	Development headers and libraries for %{name} (32-bit)
Group:		Development/C
Requires:	%{devname} = %{version}-%{release}
Requires:	%{lib32name} = %{version}-%{release}

%description -n %{dev32name}
JSON-C implements a reference counting object model that allows you to
easily construct JSON objects in C, output them as JSON formatted
strings and parse JSON formatted strings back into the C
representation of JSON objects.
%endif

%prep
%autosetup -p1

export CONFIGURE_TOP="$(pwd)"

%if %{with compat32}
%cmake32 \
	-DDISABLE_BSYMBOLIC:BOOL=OFF \
	-DENABLE_RDRAND:BOOL=ON \
	-DENABLE_THREADING:BOOL=ON \
	-G Ninja
cd ..
%endif

%cmake \
	-DDISABLE_BSYMBOLIC:BOOL=OFF \
	-DENABLE_RDRAND:BOOL=ON \
	-DENABLE_THREADING:BOOL=ON \
	-G Ninja

%build
%if %{with compat32}
%ninja_build -C build32
%endif
%ninja_build -C build

%install
%if %{with compat32}
%ninja_install -C build32
%endif
%ninja_install -C build

%files -n %{libname}
%{_libdir}/libjson-c.so.%{major}*

%files -n %{devname}
%{_libdir}/*.so
%{_includedir}/%{name}
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/json-c

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libjson-c.so.%{major}*

%files -n %{dev32name}
%{_prefix}/lib/*.so
%{_prefix}/lib/pkgconfig/*.pc
%{_prefix}/lib/cmake/json-c
%endif
