using System.Threading;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using DangerZoneCoordinatesApi.Models;

namespace DangerZoneCoordinatesApi.Data
{
    public interface IDataContext
    {
        DbSet<DangerZoneCoordinates> DangerZoneCoordinates { get; init; }
        Task<int> SaveChangesAsync(CancellationToken cancellationToken = default);
    }
}