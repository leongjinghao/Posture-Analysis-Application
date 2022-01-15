using Microsoft.EntityFrameworkCore;
using DangerZoneCoordinatesApi.Models;

namespace DangerZoneCoordinatesApi.Data
{
    public class DataContext: DbContext, IDataContext
    {
        public DataContext(DbContextOptions<DataContext> options) : base(options)
        {
             
        }
 
        public DbSet<DangerZoneCoordinates> DangerZoneCoordinates { get; init; }
    }
}