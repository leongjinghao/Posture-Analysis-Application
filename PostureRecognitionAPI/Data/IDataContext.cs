using System.Threading;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using PostureRecognitionAPI.Models;

namespace PostureRecognitionAPI.Data
{
    public interface IDataContext
    {
        DbSet<DangerZoneCoordinates> DangerZoneCoordinates { get; init; }
        DbSet<PostureLog> PostureLogs { get; init; }
        DbSet<PostureVideoPath> PostureVideoPaths { get; init; }
        Task<int> SaveChangesAsync(CancellationToken cancellationToken = default);
    }
}