%define _build_arch %(uname -i)
%define _qpid_version 1.38.0
%define _qpid_build_loc %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%define _prefix /awips2/qpid

#
# AWIPS II QPID native Spec File
#

Name: awips2-qpid-lib
Summary: AWIPS II QPID Native Library Distribution
Version: %{_qpid_version}
Release: 1%{?dist}
Group: AWIPSII
BuildRoot: %{_build_root}
BuildArch: %{_build_arch}
License:        Apache Software License
Group:          Development/Java
URL:            http://qpid.apache.org/
Packager: %{_build_site}

AutoReq: no
Provides: awips2-qpid-lib = %{_qpid_version}

BuildRequires: awips2-python
BuildRequires: boost-devel, ruby, libuuid-devel
BuildRequires: libstdc++
BuildRequires: make
BuildRequires: cmake >= 2.8.11

%description
AWIPS II QPID Lib Distribution - Contains the qpid shared libraries and
header files for qpid %{_qpid_version}.

%prep
# Ensure that a "buildroot" has been specified.
if [ "%{_build_root}" = "" ]; then
   echo "ERROR: A BuildRoot has not been specified."
   echo "FATAL: Unable to Continue ... Terminating."
   exit 1
fi

if [ -d %{_build_root} ]; then
   rm -rf %{_build_root}
fi
if [ -d %{_qpid_build_loc} ]; then
   rm -rf %{_qpid_build_loc}
fi
mkdir -p %{_qpid_build_loc}
if [ $? -ne 0 ]; then
   exit 1
fi

QPID_SOURCE_DIR="%{_baseline_workspace}/foss/qpid-lib/"
QPID_SOURCE_FILE="qpid-cpp-%{version}.tar.gz"

cp -v ${QPID_SOURCE_DIR}${QPID_SOURCE_FILE} %{_qpid_build_loc}
if [ $? -ne 0 ]; then
   exit 1
fi

pushd . > /dev/null 2>&1
cd %{_qpid_build_loc}
tar -xvzf ${QPID_SOURCE_FILE}
if [ $? -ne 0 ]; then
   exit 1
fi

popd > /dev/null 2>&1

%build
pushd . > /dev/null 2>&1

mkdir -p %{_qpid_build_loc}/build
if [ $? -ne 0 ]; then
   exit 1
fi

cd %{_qpid_build_loc}/build

%cmake %{_qpid_build_loc}/qpid-cpp-%{version} \
    -DCMAKE_VERBOSE_MAKEFILE:BOOL=OFF \
    -DBUILD_BINDING_PYTHON=OFF -DBUILD_BINDING_RUBY=OFF \
    -DBUILD_BINDING_PERL=OFF -DBUILD_BINDING_DOTNET=OFF \
    -DPYTHON_EXECUTABLE:FILEPATH=/awips2/python/bin/python \
    -DPYTHON_INCLUDE_DIR:PATH=/awips2/python/include/python2.7 \
    -DPYTHON_LIBRARY:FILEPATH=/awips2/python/lib/libpython2.7.so
if [ $? -ne 0 ]; then
   exit 1
fi

make %{?_smp_mflags} all
if [ $? -ne 0 ]; then
   exit 1
fi 
popd > /dev/null 2>&1

%install
/bin/mkdir -p %{_qpid_build_loc}/%{_prefix}
if [ $? -ne 0 ]; then
   exit 1
fi

pushd . > /dev/null 2>&1
cd %{_qpid_build_loc}/build
make DESTDIR=%{_qpid_build_loc} install
if [ $? -ne 0 ]; then
   exit 1
fi
popd > /dev/null 2>&1

/bin/mkdir -p %{_build_root}/%{_prefix}
if [ $? -ne 0 ]; then
   exit 1
fi

# copy qpid lib and include directories
/bin/cp -rv %{_qpid_build_loc}/awips2/qpid/lib \
   %{_build_root}/awips2/qpid
/bin/cp -rv %{_qpid_build_loc}/awips2/qpid/lib64/* \
   %{_build_root}/awips2/qpid/lib
/bin/cp -rv %{_qpid_build_loc}/awips2/qpid/include \
   %{_build_root}/awips2/qpid

%clean
rm -rf ${RPM_BUILD_ROOT}
rm -rf %{_qpid_build_loc}

%files
%defattr(644,awips,fxalpha,755)
/awips2/qpid/lib/*
%dir /awips2/qpid/include
/awips2/qpid/include/*
