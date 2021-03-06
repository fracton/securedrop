def test_fpf_apt_repo_present(File):
    """
    Ensure the FPF apt repo, apt.freedom.press, is configured.
    This repository is necessary for the SecureDrop Debian packages,
    including:

      * securedrop-app-code
      * securedrop-keyring
      * securedrop-grsec

    Depending on the host, additional FPF-maintained packages will be
    installed, e.g. for OSSEC. Install state for those packages
    is tested separately.
    """
    f = File('/etc/apt/sources.list.d/apt_freedom_press.list')
    assert f.contains('^deb \[arch=amd64\] https:\/\/apt\.freedom\.press '
                      'trusty main$')


def test_fpf_apt_repo_fingerprint(Command):
    """
    Ensure the FPF apt repo has the correct fingerprint on the associated
    signing pubkey. The key changed in October 2016, so test for the
    newest fingerprint, which is installed on systems via the
    `securedrop-keyring` package.
    """

    c = Command('apt-key finger')

    fpf_gpg_pub_key_info = """/etc/apt/trusted.gpg.d/securedrop-keyring.gpg
---------------------------------------------
pub   4096R/00F4AD77 2016-10-20 [expires: 2017-10-20]
      Key fingerprint = 2224 5C81 E3BA EB41 38B3  6061 310F 5612 00F4 AD77
uid                  SecureDrop Release Signing Key"""

    assert c.rc == 0
    assert fpf_gpg_pub_key_info in c.stdout

    fpf_gpg_pub_key_fingerprint_expired = ('B89A 29DB 2128 160B 8E4B  '
                                           '1B4C BADD E0C7 FC9F 6818')
    fpf_gpg_pub_key_info_expired = """pub   4096R/FC9F6818 2014-10-26 [expired: 2016-10-27]
      Key fingerprint = #{fpf_gpg_pub_key_fingerprint_expired}
uid                  Freedom of the Press Foundation Master Signing Key"""

    assert fpf_gpg_pub_key_fingerprint_expired not in c.stdout
    assert fpf_gpg_pub_key_info_expired not in c.stdout
