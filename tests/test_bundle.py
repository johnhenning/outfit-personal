import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('personal_bundle', ROOT / 'scripts/bundle.py')


class BundleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.public, self.personal = self.root / 'public', self.root / 'personal'
        self.public.mkdir()
        self.personal.mkdir()
        self.engine = str(Path(os.environ.get('OUTFIT_BINARY', ROOT.parent / 'outfit/bin/outfit')).resolve())
        self.public_data = {'schema': 1, 'name': 'Public fixture', 'roles': {'base': {'desktop': True}},
                            'profiles': {'base': {'role': 'base'}},
                            'dotfiles': [{'id': 'base-config', 'source': 'config.txt', 'target': '.config/base.conf'}]}
        self.personal_data = {'schema': 1, 'name': 'Personal fixture',
                              'profiles': {'personal': {'role': 'base', 'dotfiles': ['base-config', 'extra-config']}},
                              'dotfiles': [{'id': 'extra-config', 'source': 'extra.txt', 'target': '.config/extra.conf'}]}
        (self.public / 'config.txt').write_text('public fixture\n')
        (self.personal / 'extra.txt').write_text('personal fixture\n')
        # Unlisted files must never be published in the combined bundle.
        (self.personal / 'unlisted-secret.txt').write_text('synthetic secret\n')
        self.write_manifests()

    def write_manifests(self):
        (self.public / 'outfit.yaml').write_text(json.dumps(self.public_data))
        (self.personal / 'outfit.yaml').write_text(json.dumps(self.personal_data))

    def build(self, filename='bundle.tar.gz'):
        module = importlib.util.module_from_spec(SPEC)
        SPEC.loader.exec_module(module)
        destination = self.root / filename
        sha = module.build(self.public, self.personal, destination, self.engine)
        return destination, sha

    def test_combined_bundle_is_deterministic_allowlisted_and_usable_without_overlay(self):
        archive, sha = self.build()
        other, other_sha = self.build('second.tar.gz')
        self.assertEqual(sha, other_sha)
        self.assertEqual(sha, hashlib.sha256(archive.read_bytes()).hexdigest())
        with tarfile.open(archive) as stream:
            self.assertEqual(set(stream.getnames()), {'outfit.yaml', 'public/config.txt', 'personal/extra.txt'})
            destination = self.root / 'extracted'
            stream.extractall(destination, filter='data')
        plan = json.loads(subprocess.check_output([self.engine, 'plan', '--source', str(destination),
                                                 '--profile', 'personal', '--target', 'macos-arm64', '--json']))
        self.assertEqual({a['package_id'] for a in plan['actions'] if a['kind'] == 'dotfile'},
                         {'base-config', 'extra-config'})

    def test_conflicting_profiles_fail(self):
        self.personal_data['profiles']['base'] = {'role': 'base'}
        self.write_manifests()
        with self.assertRaises(subprocess.CalledProcessError):
            self.build()

    def test_symlink_source_fails(self):
        (self.personal / 'extra.txt').unlink()
        (self.personal / 'extra.txt').symlink_to(self.personal / 'unlisted-secret.txt')
        with self.assertRaises(subprocess.CalledProcessError):
            self.build()

    def test_traversal_source_fails(self):
        self.personal_data['dotfiles'][0]['source'] = '../unlisted-secret.txt'
        self.write_manifests()
        with self.assertRaises(subprocess.CalledProcessError):
            self.build()


class PersonalScopeTests(unittest.TestCase):
    def test_personal_profiles_select_software_without_competing_dotfile_managers(self):
        public = Path(os.environ.get('PUBLIC_PROFILES_DIRECTORY', ROOT.parent / 'outfit-profiles'))
        engine = str(Path(os.environ.get('OUTFIT_BINARY', ROOT.parent / 'outfit/bin/outfit')).resolve())
        for profile in ('john-mac-everyday', 'john-mac-dev', 'john-dev', 'john-compute', 'john-media'):
            with self.subTest(profile=profile):
                plan = json.loads(subprocess.check_output([
                    engine, 'plan', '--source', str(public), '--personal', str(ROOT),
                    '--profile', profile, '--target', 'macos-arm64', '--json']))
                self.assertTrue(plan['actions'])
                self.assertFalse(any(action['kind'] == 'dotfile' for action in plan['actions']))


if __name__ == '__main__':
    unittest.main()
