using System.Collections.Generic;
using System.Threading.Tasks;
using DangerZoneCoordinatesApi.Models;

namespace DangerZoneCoordinatesApi.Repositories
{
    public interface IDangerZoneCoordinatesRepository
    {
        Task<IEnumerable<DangerZoneCoordinates>> GetAll(int cameraId);
        Task<IEnumerable<DangerZoneCoordinates>> GetAll();
        Task Add(DangerZoneCoordinates dangerZoneCoordinates);
        Task Delete(int id);
        Task Update(DangerZoneCoordinates dangerZoneCoordinates);
    }
}