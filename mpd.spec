%define build_plf 0
%{?_with_plf: %{expand: %%global build_plf 1}}

%if %build_plf  
%define distsuffix plf
%endif

Summary:		MPD, the Music Player Daemon
Name:			mpd
Version:		0.13.0
Release:		%mkrel 3
License:		GPL
Group:			Sound
URL:			http://www.musicpd.org/
Source:			http://www.musicpd.org/uploads/files/%{name}-%{version}.tar.bz2
Source1:		%{name}.conf
Source2:		%{name}.init
Source3:		%{name}.logrotate
Source4:		README.urpmi
Requires(pre):		rpm-helper
Requires(post):         rpm-helper
Requires(preun):        rpm-helper
Requires(postun):       rpm-helper
BuildRequires:		libalsa-devel
BuildRequires:		libavahi-common-devel
BuildRequires:	        libogg-devel
BuildRequires:	        libvorbis-devel
BuildRequires:	        libflac-devel libflac++-devel
BuildRequires:	        libaudiofile-devel
BuildRequires:	        libmikmod-devel
BuildRequires:	        libmad-devel
BuildRequires:	        libid3tag-devel
BuildRequires:		libatomic_ops-devel
BuildRequires:		libshout-devel
BuildRequires:          libjack-devel
BuildRequires:          libao-devel
BuildRequires:          libpulseaudio-devel
BuildRequires:          libmpcdec-devel
%if %build_plf
BuildRequires:          libfaad2-devel
%endif
BuildRoot:		%{_tmppath}/%{name}-%{version}-buildroot

%if %build_plf
%description
Music Player Daemon (MPD) allows remote access for playing music (MP3, Ogg
Vorbis, FLAC, Mod, and wave files) and managing playlists. MPD is designed
for integrating a computer into a stereo system that provides control for music
playback over a local network. It is also makes a great desktop music player,
especially if your a console junkie, like frontend options, or restart X often.
This plf version of MPD add AAC files support by using libfaad2_0.

%else
%description
Music Player Daemon (MPD) allows remote access for playing music (MP3, Ogg
Vorbis, FLAC, Mod, and wave files) and managing playlists. MPD is designed
for integrating a computer into a stereo system that provides control for music
playback over a local network. It is also makes a great desktop music player,
especially if your a console junkie, like frontend options, or restart X often.
%endif

%prep
%setup -q

%build
%if %build_plf
%configure2_5x --with-alsa-prefix=%{_prefix}
%else
%configure2_5x --disable-aac --with-alsa-prefix=%{_prefix}
%endif
%make

%install
rm -rf %{buildroot}
%makeinstall_std

mkdir -p %{buildroot}/var/lib/mpd
touch %{buildroot}/%{_localstatedir}/mpd/mpd.db
touch %{buildroot}/%{_localstatedir}/mpd/mpdstate
mkdir -p %{buildroot}/var/log/mpd
touch %{buildroot}/var/log/mpd/mpd.log
touch %{buildroot}/var/log/mpd/mpd.error
mkdir -p %{buildroot}/var/run/mpd
mkdir -p %{buildroot}/%{_localstatedir}/mpd/playlists
mkdir -p %{buildroot}/%{_localstatedir}/mpd/music

install -D %{SOURCE1} %{buildroot}/etc/mpd.conf
install -D %{SOURCE2} %{buildroot}/%{_initrddir}/%{name}
install -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install %{SOURCE4} doc/README.urpmi
rm -rf %{buildroot}/%{_docdir}/mpd

%clean
rm -rf %{buildroot}

%pre
%_pre_useradd %name %{_localstatedir}/%{name} /bin/false
usermod -g audio %{name}

%post
if [ $1 -eq 1 ]
then
%create_ghostfile %{_localstatedir}/mpd/mpd.db mpd audio 644
%create_ghostfile %{_localstatedir}/mpd/mpdstate mpd audio 644
%create_ghostfile /var/log/mpd/mpd.log mpd audio 644
%create_ghostfile /var/log/mpd/mpd.error mpd audio 644
service %{name} createdb
fi
#echo If you want to run mpd as a service, please read
#echo /usr/share/doc/mpd-%{version}/README.MDK
%_post_service %{name}

%preun
%_preun_service %{name}

%postun
%_postun_userdel %{name}

%files
%defattr(-,root,root)
%doc README UPGRADING doc/COMMANDS AUTHORS COPYING ChangeLog doc/mpdconf.example doc/*.urpmi
%{_bindir}/%{name}
%{_mandir}/man1/*
%{_mandir}/man5/*
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(-,mpd,root) %config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_initrddir}/%{name}
%defattr(644,mpd,audio)
%attr(755,mpd,audio) %dir %{_localstatedir}/mpd
%attr(755,mpd,audio) %dir %{_localstatedir}/mpd/music
%attr(755,mpd,audio) %dir %{_localstatedir}/mpd/playlists
%ghost %{_localstatedir}/mpd/mpd.db
%ghost %{_localstatedir}/mpd/mpdstate
%attr(755,mpd,audio) %dir /var/log/mpd
%attr(755,mpd,audio) %dir /var/run/mpd
%ghost /var/log/mpd/mpd.log
%ghost /var/log/mpd/mpd.error
