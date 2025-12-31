from django.core.management.base import BaseCommand
from django.core.cache import cache


class Command(BaseCommand):
    help = 'Clear Redis cache with various options'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            help='Clear all cache',
        )
        parser.add_argument(
            '--pattern',
            type=str,
            help='Clear cache matching pattern',
        )
        parser.add_argument(
            '--stats',
            action='store_true',
            help='Show cache statistics',
        )

    def handle(self, *args, **options):
        if options['stats']:
            self.show_stats()
        elif options['all']:
            self.clear_all()
        elif options['pattern']:
            self.clear_pattern(options['pattern'])
        else:
            self.stdout.write(self.style.WARNING('No action specified. Use --help for options.'))

    def clear_all(self):
        cache.clear()
        self.stdout.write(self.style.SUCCESS('✓ All cache cleared successfully'))

    def clear_pattern(self, pattern):
        try:
            deleted = cache.delete_pattern(pattern)
            self.stdout.write(self.style.SUCCESS(f'✓ Cleared {deleted} keys matching pattern: {pattern}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error clearing pattern: {e}'))

    def show_stats(self):
        try:
            from django_redis import get_redis_connection
            redis_conn = get_redis_connection('default')
            info = redis_conn.info()
            
            self.stdout.write(self.style.SUCCESS('\n=== Redis Cache Statistics ==='))
            self.stdout.write(f"Used Memory: {info.get('used_memory_human', 'N/A')}")
            self.stdout.write(f"Max Memory: {info.get('maxmemory_human', 'N/A')}")
            self.stdout.write(f"Total Keys: {redis_conn.dbsize()}")
            self.stdout.write(f"Keyspace Hits: {info.get('keyspace_hits', 0)}")
            self.stdout.write(f"Keyspace Misses: {info.get('keyspace_misses', 0)}")
            
            hits = info.get('keyspace_hits', 0)
            misses = info.get('keyspace_misses', 0)
            total = hits + misses
            if total > 0:
                hit_rate = (hits / total) * 100
                self.stdout.write(f"Hit Rate: {hit_rate:.2f}%")
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error getting stats: {e}'))
