using Microsoft.EntityFrameworkCore;
using PostureRecognitionAPI.Models;

namespace PostureRecognitionAPI.Data
{
    public class DataContext : DbContext, IDataContext
    {
        public DataContext(DbContextOptions<DataContext> options) : base(options)
        {
             
        }
 
        public DbSet<DangerZoneCoordinates> DangerZoneCoordinates { get; init; }
        public DbSet<PostureLog> PostureLogs { get; init; }
        public DbSet<PostureVideoPath> PostureVideoPaths { get; init; }
    }
}