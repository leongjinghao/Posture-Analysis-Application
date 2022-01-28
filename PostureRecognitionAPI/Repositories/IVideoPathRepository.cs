using System.Collections.Generic;
using System.Threading.Tasks;
using PostureRecognitionAPI.Models;

namespace PostureRecognitionAPI.Repositories
{
    public interface IVideoPathRepository
    {
        Task<VideoPath> Get(int id);
        Task<IEnumerable<VideoPath>> GetAll();
        Task Add(VideoPath videoPath);
        Task Delete(int id);
        Task Update(VideoPath videoPath);
    }
}