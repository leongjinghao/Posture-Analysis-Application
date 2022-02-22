using System.Collections.Generic;
using System.Threading.Tasks;
using PostureRecognitionAPI.Models;

namespace PostureRecognitionAPI.Repositories
{
    public interface IPostureVideoPathRepository
    {
        Task<PostureVideoPath> Get(int id);
        Task<IEnumerable<PostureVideoPath>> GetAll();
        Task Add(PostureVideoPath postureVideoPath);
        Task Delete(string videoName);
        Task Update(PostureVideoPath postureVideoPath);
    }
}