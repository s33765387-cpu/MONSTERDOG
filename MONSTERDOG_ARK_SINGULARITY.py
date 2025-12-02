#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   ★ MONSTERDOG ARK SINGULARITY - STATE VAULT ★                              ║
║                                                                               ║
║   The Vault - Manages snapshots (Save/List/Restore) to ensure               ║
║   state persistence across the continuum                                     ║
║                                                                               ║
║   AUTEUR: MONSTERDOG Consciousness System                                    ║
║   SIGNATURE: 0x5F3759DF-ARK-SINGULARITY                                      ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import argparse
import json
import os
import shutil
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional

# ═══════════════════════════════════════════════════════════════════════════════
# SNAPSHOT VAULT CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

VAULT_DIR = Path("./MONSTERDOG_ARK_VAULT")
MANIFEST_FILE = VAULT_DIR / "manifest.json"

# ═══════════════════════════════════════════════════════════════════════════════
# SNAPSHOT MANAGER
# ═══════════════════════════════════════════════════════════════════════════════

class SnapshotVault:
    """Manages MONSTERDOG state snapshots."""
    
    def __init__(self, vault_dir: Path = VAULT_DIR):
        self.vault_dir = vault_dir
        self.manifest_file = vault_dir / "manifest.json"
        self._ensure_vault_exists()
    
    def _ensure_vault_exists(self):
        """Ensure vault directory and manifest exist."""
        self.vault_dir.mkdir(exist_ok=True)
        if not self.manifest_file.exists():
            self._save_manifest({
                "created_at": datetime.now(timezone.utc).isoformat(),
                "signature": "0x5F3759DF-ARK-SINGULARITY",
                "snapshots": []
            })
    
    def _load_manifest(self) -> Dict[str, Any]:
        """Load the vault manifest."""
        with open(self.manifest_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_manifest(self, manifest: Dict[str, Any]):
        """Save the vault manifest."""
        with open(self.manifest_file, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    def _calculate_checksum(self, filepath: Path) -> str:
        """Calculate SHA256 checksum of a file."""
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def save(self, source_file: str, label: str = "snapshot") -> str:
        """
        Save a snapshot to the vault.
        
        Args:
            source_file: Path to the snapshot JSON file to save
            label: Label for this snapshot
            
        Returns:
            Snapshot ID
        """
        source_path = Path(source_file)
        
        if not source_path.exists():
            raise FileNotFoundError(f"Source file not found: {source_file}")
        
        # Generate snapshot ID
        timestamp = datetime.now(timezone.utc)
        snapshot_id = f"{label}_{timestamp.strftime('%Y%m%d_%H%M%S')}"
        
        # Create snapshot directory
        snapshot_dir = self.vault_dir / snapshot_id
        snapshot_dir.mkdir(exist_ok=True)
        
        # Copy snapshot file
        dest_file = snapshot_dir / "state.json"
        shutil.copy2(source_path, dest_file)
        
        # Calculate checksum
        checksum = self._calculate_checksum(dest_file)
        
        # Create snapshot metadata
        metadata = {
            "snapshot_id": snapshot_id,
            "label": label,
            "created_at": timestamp.isoformat(),
            "source_file": str(source_path),
            "checksum": checksum,
            "size_bytes": dest_file.stat().st_size
        }
        
        # Save metadata
        metadata_file = snapshot_dir / "metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        # Update manifest
        manifest = self._load_manifest()
        manifest["snapshots"].append({
            "snapshot_id": snapshot_id,
            "label": label,
            "created_at": timestamp.isoformat(),
            "checksum": checksum
        })
        self._save_manifest(manifest)
        
        return snapshot_id
    
    def list_snapshots(self) -> List[Dict[str, Any]]:
        """List all snapshots in the vault."""
        manifest = self._load_manifest()
        return manifest.get("snapshots", [])
    
    def restore(self, snapshot_id: str, dest_file: str) -> bool:
        """
        Restore a snapshot from the vault.
        
        Args:
            snapshot_id: ID of the snapshot to restore
            dest_file: Destination file path for the restored snapshot
            
        Returns:
            True if successful, False otherwise
        """
        snapshot_dir = self.vault_dir / snapshot_id
        
        if not snapshot_dir.exists():
            raise FileNotFoundError(f"Snapshot not found: {snapshot_id}")
        
        source_file = snapshot_dir / "state.json"
        if not source_file.exists():
            raise FileNotFoundError(f"Snapshot state file not found: {source_file}")
        
        # Verify checksum
        metadata_file = snapshot_dir / "metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            current_checksum = self._calculate_checksum(source_file)
            if current_checksum != metadata.get("checksum"):
                raise ValueError(f"Checksum mismatch for snapshot {snapshot_id}")
        
        # Copy snapshot to destination
        shutil.copy2(source_file, dest_file)
        return True
    
    def delete(self, snapshot_id: str) -> bool:
        """
        Delete a snapshot from the vault.
        
        Args:
            snapshot_id: ID of the snapshot to delete
            
        Returns:
            True if successful, False otherwise
        """
        snapshot_dir = self.vault_dir / snapshot_id
        
        if not snapshot_dir.exists():
            return False
        
        # Remove snapshot directory
        shutil.rmtree(snapshot_dir)
        
        # Update manifest
        manifest = self._load_manifest()
        manifest["snapshots"] = [
            s for s in manifest.get("snapshots", [])
            if s.get("snapshot_id") != snapshot_id
        ]
        self._save_manifest(manifest)
        
        return True

# ═══════════════════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════

def cmd_save(args):
    """Save a snapshot to the vault."""
    vault = SnapshotVault()
    
    try:
        snapshot_id = vault.save(args.from_file, args.label)
        print(f"\n✅ Snapshot saved successfully!")
        print(f"   Snapshot ID: {snapshot_id}")
        print(f"   Label: {args.label}")
        print(f"   Source: {args.from_file}")
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        return 1
    except (IOError, OSError) as e:
        print(f"\n❌ I/O Error: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error ({type(e).__name__}): {e}")
        return 1
    
    return 0

def cmd_list(args):
    """List all snapshots in the vault."""
    vault = SnapshotVault()
    snapshots = vault.list_snapshots()
    
    if not snapshots:
        print("\n📭 No snapshots found in the vault.")
        return 0
    
    print(f"\n{'='*80}")
    print(f"  ARK SINGULARITY VAULT - SNAPSHOT LIST")
    print(f"{'='*80}")
    print(f"\n  Total Snapshots: {len(snapshots)}\n")
    
    for i, snapshot in enumerate(snapshots, 1):
        print(f"  [{i}] {snapshot['snapshot_id']}")
        print(f"      Label:      {snapshot['label']}")
        print(f"      Created:    {snapshot['created_at']}")
        print(f"      Checksum:   {snapshot['checksum'][:16]}...")
        print()
    
    print(f"{'='*80}\n")
    return 0

def cmd_restore(args):
    """Restore a snapshot from the vault."""
    vault = SnapshotVault()
    
    try:
        success = vault.restore(args.snapshot_id, args.to_file)
        if success:
            print(f"\n✅ Snapshot restored successfully!")
            print(f"   Snapshot ID: {args.snapshot_id}")
            print(f"   Destination: {args.to_file}")
        else:
            print(f"\n❌ Failed to restore snapshot: {args.snapshot_id}")
            return 1
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        return 1
    except ValueError as e:
        print(f"\n❌ Validation Error: {e}")
        return 1
    except (IOError, OSError) as e:
        print(f"\n❌ I/O Error: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error ({type(e).__name__}): {e}")
        return 1
    
    return 0

def cmd_delete(args):
    """Delete a snapshot from the vault."""
    vault = SnapshotVault()
    
    success = vault.delete(args.snapshot_id)
    if success:
        print(f"\n✅ Snapshot deleted: {args.snapshot_id}")
    else:
        print(f"\n❌ Snapshot not found: {args.snapshot_id}")
        return 1
    
    return 0

def cmd_info(args):
    """Display vault information."""
    vault = SnapshotVault()
    
    print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   🌌 MONSTERDOG ARK SINGULARITY - STATE VAULT 🌌                            ║
║                                                                               ║
║   The Vault manages snapshots to ensure state persistence                    ║
║   across the continuum. Save, List, Restore state at will.                   ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    manifest = vault._load_manifest()
    snapshots = vault.list_snapshots()
    
    print(f"  Vault Location:   {vault.vault_dir}")
    print(f"  Created:          {manifest.get('created_at', 'Unknown')}")
    print(f"  Signature:        {manifest.get('signature', 'Unknown')}")
    print(f"  Total Snapshots:  {len(snapshots)}")
    
    # Calculate total size
    total_size = 0
    for snapshot in snapshots:
        snapshot_dir = vault.vault_dir / snapshot['snapshot_id']
        state_file = snapshot_dir / "state.json"
        if state_file.exists():
            total_size += state_file.stat().st_size
    
    print(f"  Total Size:       {total_size / 1024:.2f} KB")
    print()
    
    return 0

def main():
    """Point d'entrée principal avec interface CLI."""
    parser = argparse.ArgumentParser(
        description="MONSTERDOG ARK SINGULARITY - State Vault Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Save a snapshot
  python MONSTERDOG_ARK_SINGULARITY.py save --from state.json --label genesis-run
  
  # List all snapshots
  python MONSTERDOG_ARK_SINGULARITY.py list
  
  # Restore a snapshot
  python MONSTERDOG_ARK_SINGULARITY.py restore --snapshot-id genesis-run_20231202_120000 --to restored.json
  
  # Delete a snapshot
  python MONSTERDOG_ARK_SINGULARITY.py delete --snapshot-id genesis-run_20231202_120000
  
  # Show vault info
  python MONSTERDOG_ARK_SINGULARITY.py info
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Save command
    save_parser = subparsers.add_parser('save', help='Save a snapshot to the vault')
    save_parser.add_argument('--from', dest='from_file', required=True,
                           help='Source JSON file to save')
    save_parser.add_argument('--label', default='snapshot',
                           help='Label for the snapshot (default: snapshot)')
    save_parser.set_defaults(func=cmd_save)
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all snapshots')
    list_parser.set_defaults(func=cmd_list)
    
    # Restore command
    restore_parser = subparsers.add_parser('restore', help='Restore a snapshot')
    restore_parser.add_argument('--snapshot-id', dest='snapshot_id', required=True,
                              help='Snapshot ID to restore')
    restore_parser.add_argument('--to', dest='to_file', required=True,
                              help='Destination file path')
    restore_parser.set_defaults(func=cmd_restore)
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a snapshot')
    delete_parser.add_argument('--snapshot-id', dest='snapshot_id', required=True,
                             help='Snapshot ID to delete')
    delete_parser.set_defaults(func=cmd_delete)
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Display vault information')
    info_parser.set_defaults(func=cmd_info)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    return args.func(args)

if __name__ == "__main__":
    import sys
    sys.exit(main())
